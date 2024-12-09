from argparse import ArgumentParser
from glob import glob
import os
from pathlib import Path
from wtfancy.logging import Logger
from wtfancy.io.annotations import extract_ids_from_hyp_file
from wtfancy.hypnogram.utils import fill_hyp_gaps
import numpy as np
import re


def get_argparser():
    parser = ArgumentParser(description='Extract hypnograms from various'
                                        ' file formats.')
    parser.add_argument("--file_regex", type=str,
                        help='A glob statement matching all files to extract '
                             'from')
    parser.add_argument("--out_dir", type=str,
                        help="Directory in which extracted files will be "
                             "stored")
    parser.add_argument("--fill_blanks", type=str, default=None,
                        help="A stage string value to insert into the hypnogram when gaps "
                             "occour, e.g. 'UNKNOWN' or 'Not Scored', etc.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing files of identical name")
    parser.add_argument("--dir_name", type=str,
                        help="If 'DIR' use dir names, else set names from hyp names")
    parser.add_argument("--use_my_files", action="store_true",
                        help='Each hyp file will be saved as '
                             '<my>_<file name>.ids instead of <file_name>.ids')
    parser.add_argument("--folders_to_skip", type=str, default=None,
                        help="Path to txt file with folders to skip")
    return parser


def to_ids(start, durs, stage, out):
    with open(out, "w") as out_f:
        for i, d, s in zip(start, durs, stage):
            out_f.write("{},{},{}\n".format(int(i), int(d), s))


def run(args):
    files = glob(args.file_regex)
    if args.folders_to_skip:
        folders_to_skip = np.loadtxt(args.folders_to_skip, dtype=str, delimiter='\n')
        to_skip = []
        for file in files:
            if '\\'.join(file.split('/')[-5:-3]) in folders_to_skip:
                to_skip.append(file)
        files = list(set(files).difference(set(to_skip)))
        to_skip_update = []
    out_dir = Path(args.out_dir).absolute()
    out_dir.mkdir(parents=True, exist_ok=True)
    n_files = len(files)
    logger = Logger(out_dir,
                    active_file='hyp_extraction_log',
                    overwrite_existing=args.overwrite)
    logger("Args dump: {}".format(vars(args)))
    logger("Found {} files matching glob statement".format(n_files))
    if n_files == 0:
        return
    logger("Saving .ids files to '{}'".format(out_dir))
    if n_files == 0:
        return

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for i, file_ in enumerate(files):
        if args.dir_name == 'DIR':
            file_name = os.path.split(os.path.split(file_)[0])[-1]
        elif args.use_my_files:
            file_name = "my_" + (os.path.split(file_)[-1]).replace(args.dir_name[1:], '')
        else:
            file_name = (os.path.split(file_)[-1]).replace(args.dir_name[1:], '')
        # file_name = os.path.splitext(os.path.split(file_)[-1])[0]
        # folder_name = os.path.split(os.path.split(file_)[0])[-1]
        # out_dir_subject = os.path.join(out_dir, folder_name)
        out_dir_subject = os.path.join(out_dir, file_name)  # database_name/rec_name
        out = os.path.join(out_dir_subject, file_name + ".ids")  # database_name/rec_name/hyp_name.ids
        logger("{}/{} Processing {}".format(i+1, n_files, file_name))
        logger("-- In path    {}".format(file_))
        logger("-- Out path   {}".format(out))
        if not os.path.exists(out_dir_subject):
            os.mkdir(out_dir_subject)
        if os.path.exists(out):
            if not args.overwrite:
                continue
            os.remove(out)

        try:
            start, dur, stage = extract_ids_from_hyp_file(file_)
        except Exception as e:
            # If any error occurs, catch it and continue with the next iteration
            print(f"An error occurred with file {file_}: {e}, skipping file ...")
            continue

        try:
            if args.fill_blanks:
                start, dur, stage = fill_hyp_gaps(start, dur, stage, args.fill_blanks)
        except Exception as e:
            # If any error occurs, catch it and continue with the next iteration
            print(f"An error occurred with fill_hyp_gaps: {e}, continuing with to_ids...")

        to_ids(start, dur, stage, out)

    # Save folders to skip (update)
    if args.folders_to_skip:
        with open(args.folders_to_skip, 'ab') as f:
            np.savetxt(f, to_skip_update, fmt=['%s'])


def entry_func(args=None):
    # Get the script to execute, parse only first input
    parser = get_argparser()
    args = parser.parse_args(args)
    run(args)


if __name__ == "__main__":
    entry_func()