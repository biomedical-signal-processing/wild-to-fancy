"""
Small utility script that extracts a set of channels from a set of data files
and saves them to a folder in .h5 files with minimally required header info
attached as h5 attributes (sample rate etc.).

The file must be loadable using:
wtfancy.io.high_level_file_loaders import load_data_file
"""

from argparse import ArgumentParser
from glob import glob
import os
from wtfancy.errors import ChannelNotFoundError
from wtfancy.io.channels import ChannelMontageTuple, ChannelMontageCreator
from wtfancy.io.channels import auto_infer_referencing as infer_channel_refs
from wtfancy.io.channels import infer_channel_types
from wtfancy.io.header import extract_header
from wtfancy.logging import Logger


def get_argparser():
    """
    Returns an argument parser for this script
    """
    parser = ArgumentParser(description='Extract a set of channels from a set '
                                        'of PSG files, various formats '
                                        'supported. The extracted data will be'
                                        ' saved to .h5 files with minimal '
                                        'header information attributes.')
    parser.add_argument("--file_regex", type=str,
                        help='A glob statement matching all files to extract '
                             'from')
    parser.add_argument("--out_dir", type=str,
                        help="Directory in which extracted files will be "
                             "stored")
    parser.add_argument("--channels", nargs="+", type=str,
                        help="Space-separated list of CHAN1-CHAN2 format of"
                             "referenced channel montages to extract. A "
                             "montage will be created if the referenced "
                             "channel is not already available in the file. If"
                             " the channel does not already exist and if "
                             "CHAN1 or CHAN2 is not available, an error is "
                             "raised.")
    parser.add_argument("--rename_channels", nargs="+", type=str,
                        help="Space-separated list of channel names to save"
                             " as instead of the originally extracted names. "
                             "Must match in length --channels.")
    parser.add_argument("--select_types", type=str, nargs="+", default=None,
                        help='A list of channel types (e.g., EEG EOG, MASTOID) to select' )
    parser.add_argument("--auto_reference_types", type=str, nargs="+", default=None,
                        help='A list of channel types (e.g., EEG EOG) to select')
    parser.add_argument('--resample', type=int, default=None,
                        help='Re-sample the selected channels before storage.')
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files of identical name")
    parser.add_argument("--use_dir_names", action="store_true",
                        help='Each PSG file will be saved as '
                             '<parent directory>.h5 instead of <file_name>.h5')
    parser.add_argument("--use_my_files", action="store_true",
                        help='Each PSG file will be saved as '
                             '<my>_<file name>.h5 instead of <file_name>.h5')
    parser.add_argument("--del_nsrr_names", action="store_true",
                        help='Delete "-nsrr" from Each PSG')
    parser.add_argument("--folders_to_skip", type=str, default=None,
                        help="Path to txt file with folders to skip")
    return parser


def filter_channels(renamed_channels, selected_original_channels,
                    original_channels):
    inds_selected = [i for i, chan in enumerate(original_channels)
                     if chan in selected_original_channels]
    return [chan for i, chan in enumerate(renamed_channels)
            if i in inds_selected]


def _extract(file_,
             out_path,
             channels,
             renamed_channels,
             logger,
             args):
    from wtfancy.io.high_level_file_loaders import load_data
    from wtfancy.utils.scriptutils import to_h5_file

    channels_in_file = extract_header(file_)["channel_names"]

    chan_creator = ChannelMontageCreator(existing_channels=channels_in_file,
                                         channels_required=channels,
                                         allow_missing=True)
    logger("[*] Channels in file: " + ", ".join(chan_creator.existing_channels.names))
    logger("[*] Output channels: " + ", ".join(chan_creator.output_channels.names))
    logger("[*] Channels to load: " + ", ".join(chan_creator.channels_to_load.names))
    try:
        data, header = load_data(file_, chan_creator.channels_to_load,
                               check_num_channels=False)
    except ChannelNotFoundError as e:
        logger("\n-----\nCHANNEL ERROR ON FILE {}".format(file_))
        logger(str(e) + "\n-----")
        os.rmdir(os.path.split(out_path)[0])
        return

    # create montages
    data, channels = chan_creator.create_montages(data)
    header['channel_names'] = channels

    # Resample
    logger("[*] Data shape before re-sampling: {}".format(data.shape))
    if args.resample:
        from wtfancy.preprocessing.data_sampling import set_data_sample_rate
        data = set_data_sample_rate(data,
                                  new_sample_rate=args.resample,
                                  old_sample_rate=header['sample_rate'])
        header['sample_rate'] = args.resample
        if data.shape[0] % args.resample:
            logger("ERROR: Not divisible by sample rate!")
    logger("[*] Data shape after re-sampling: {}".format(data.shape))

    # Rename channels
    if renamed_channels:
        org_names = header['channel_names'].original_names
        header['channel_names'] = filter_channels(renamed_channels,
                                                  org_names,
                                                  args.channels)
    else:
        header['channel_names'] = header['channel_names'].original_names
    logger("[*] Extracted {} channels: {}".format(data.shape[1],
                                                  header['channel_names']))
    to_h5_file(out_path, data, **header)


def extract(files, out_dir, channels, renamed_channels, logger, args):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for i, file_ in enumerate(files):
        if args.use_dir_names:
            name = os.path.split(os.path.split(file_)[0])[-1]  # name of the folder containing edf file
        elif args.use_my_files:
            name = "my_" + os.path.splitext(os.path.split(file_)[-1])[0]
        else:
            name = os.path.splitext(os.path.split(file_)[-1])[0]  # name of the edf file without '.edf'
            if args.del_nsrr_names:
                name = name.replace('-nsrr', '')
        logger("------------------")
        logger("[*] {}/{} Processing {}".format(i + 1, len(files), name))
        out_dir_subject = os.path.join(out_dir, name)  # database_name/rec_name
        if not os.path.exists(out_dir_subject):
            os.mkdir(out_dir_subject)
        out_path = os.path.join(out_dir_subject, name + ".h5")  # database_name/rec_name/rec_name.h5
        if os.path.exists(out_path):
            if not args.overwrite:
                logger("-- Skipping (already exists, overwrite=False)")
                continue
            os.remove(out_path)
        try:
            _extract(
                file_=file_,
                out_path=out_path,
                channels=channels,
                renamed_channels=renamed_channels,
                logger=logger,
                args=args
            )
        except Exception as e:
            # If any error occurs, catch it and continue with the next iteration
            print(f"An error occurred with file {file_}: {e}, skipping file ...")


def run(args):
    files = glob(args.file_regex)
    if args.folders_to_skip:
        import numpy as np
        folders_to_skip = np.loadtxt(args.folders_to_skip, dtype=str, delimiter='\n')
        to_skip = []
        for file in files:
            if '\\'.join(file.split('/')[-5:-3]) in folders_to_skip:
                to_skip.append(file)
        files = list(set(files).difference(set(to_skip)))
    out_dir = os.path.abspath(args.out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    logger = Logger(out_dir,
                    active_file='extraction_log',
                    overwrite_existing=args.overwrite,
                    print_calling_method=False)
    logger("Args dump: {}".format(vars(args)))
    logger("Found {} files matching glob statement".format(len(files)))
    if len(files) == 0:
        return

    if args.select_types:
        # Search channels to include in the extraction process
        select_types = [type_.upper().strip() for type_ in (args.select_types or [])]
        selected = []
        ch_types = []
        for file_ in files:
            # logger(f"File: {file_}")
            header = extract_header(file_)
            inferred_types = infer_channel_types(header['channel_names'])
            for name, type_ in zip(header['channel_names'], inferred_types):
                if type_ in select_types and name not in selected:
                    selected.append(f"{name}")
                    ch_types.append(f"{type_}")
                # logger(f"{name} ({type_}?)")
            if selected:
                # logger(f"Selected: {' '.join(selected)}")
                args.channels = selected
            else:
                raise ValueError(
                    f"No valid signal was found in file: {file_} based on the provided select_types: "
                    f"{', '.join(select_types)}")

            logger(f"\nFound:\n"
                        f"-- Selected channels: {selected}\n")

            if args.auto_reference_types:
                args.channels, _ = infer_channel_refs(channel_names=args.channels,
                                                                     channel_types=ch_types,
                                                                     types=args.auto_reference_types,
                                                                     on_already_ref="warn")

    channels = ChannelMontageTuple(args.channels, relax=True)

    renamed_channels = args.rename_channels
    if renamed_channels and (len(renamed_channels) != len(channels)):
        raise ValueError("--rename_channels argument must have the same number"
                         " of elements as --channels. Got {} and {}.".format(
            len(channels), len(renamed_channels)
        ))

    logger("Extracting channels {}".format(channels.names))
    if renamed_channels:
        logger("Saving channels under names {}".format(renamed_channels))
    logger("Saving .h5 files to '{}'".format(out_dir))
    logger("Re-sampling: {}".format(args.resample))
    logger("-*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-")
    extract(
        files=files,
        out_dir=out_dir,
        channels=channels,
        renamed_channels=renamed_channels,
        logger=logger,
        args=args
    )


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    entry_func()
