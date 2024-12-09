"""
A collection of high level of data loader functions for data and annotations files

This file should contain only the following functions:

- load_data(file_path, *args, **kwargs) --> data_array, data_header
- load_annotations(file_path, *args, **kwargs) --> annotation, annotation dict
"""

import h5py
from wtfancy.io.data import extract_data
from wtfancy.io.annotations import extract_ann_data
from wtfancy.io.header import extract_header
from wtfancy.io.channels.utils import get_org_include_exclude_channel_montages
from wtfancy.errors import ChannelNotFoundError


def load_data(data_file_path,
             load_channels=None,
             ignore_reference_channels=False,
             load_time_channel_selector=None,
             check_num_channels=True):
    """
    Returns a numpy object of shape NxC (N data points, C channels) and a
    dictionary of header information as given by 'extract_header'.

    Args:
        file_path: Path to data file
        load_channels: A list of channel name strings or a ChannelMontageTuple
                       storing ChannelMontage objects representing all channels
                       to load.
        ignore_reference_channels: TODO
        load_time_channel_selector: TODO
        check_num_channels: TODO

    Returns:
        A numpy array of shape NxC (N samples, C channels)
        A dictionary of header information
    """
    # Load the header of a data file. Stores e.g. channel names and sample rates
    header = extract_header(data_file_path)

    if load_time_channel_selector:
        # Randomly select from the available channels in groups according to
        # passed RandomChannelSelector object
        if load_channels is not None:
            raise ValueError("Must not specify the 'load_channels' argument "
                             "with the 'load_time_channel_selector' argument.")
        try:
            load_channels = load_time_channel_selector.sample(
                available_channels=header["channel_names"]
            )
        except ChannelNotFoundError as e:
            raise ChannelNotFoundError(
                "The data file at path {} is missing channels according to one "
                "or multiple of the specified channel sampling groups. "
                "File has: {}, requested groups: {}"
                "".format(data_file_path, header['channel_names'],
                          load_time_channel_selector.channel_groups)) from e

    # Work out which channels to include and exclude during loading
    org_channels, include_channels, exclude_channels = \
        get_org_include_exclude_channel_montages(
            load_channels=load_channels,
            header=header,
            ignore_reference_channels=ignore_reference_channels,
            check_num_channels=check_num_channels,
            check_duplicates=True
        )
    header["channel_names"] = include_channels
    header["n_channels"] = len(include_channels)

    # Actually load data from disk, if not done already in open_data_file
    # Select the relevant channels if not done already in open_data_file
    data = extract_data(data_file_path, header,
                                include_channels=include_channels.original_names,
                                exclude_channels=exclude_channels.original_names)
    return data, header


def load_annotations(file_path, period_length_sec, annotation_dict, sample_rate):
    """
    Returns a wtfancy.* AnnType object representation of the
    labels data at path 'file_path'.

    Args:
        file_path:          A string path pointing to the file to load
        period_length_sec:  The period length in seconds
        annotation_dict:    A dictionary mapping labels as stored in
                            'file_path' to integer label values. Can be None,
                            in which case a default or automatically inferred
                            annotation_dict will be used.
        sample_rate:        The sample of the original signal
                            used in rare cases e.g. to convert a 'signal dense' hypnogram
                            (see utime.hypnogram.utils).

    Returns:
        A SparseHypnogram object
        A dictionary annotation_dict. Will be identical to the passed
        annotation_dict unless None was passed for annotation_dict, in which
        case the returned annotation_dict will be the automatically inferred
    """
    ann, annotation_dict = extract_ann_data(file_path=file_path,
                                            period_length_sec=period_length_sec,
                                            annotation_dict=annotation_dict,
                                            sample_rate=sample_rate)
    return ann, annotation_dict


def open_h5_archive(h5_file_path,
                    load_channels=None,
                    ignore_reference_channels=False,
                    check_num_channels=True,
                    dataset_name='channels'):
    # Open archive
    h5_obj = h5py.File(h5_file_path, "r")

    # Get channels in file
    header = {'channel_names': list(h5_obj[dataset_name].keys())}

    # Work out which channels to include and exclude during loading
    org_channels, include_channels, _ = \
        get_org_include_exclude_channel_montages(
            load_channels=load_channels,
            header=header,
            ignore_reference_channels=ignore_reference_channels,
            check_num_channels=check_num_channels
        )
    data = {}
    for chnl in include_channels:
        data[chnl] = h5_obj[dataset_name][chnl.original_name]
    return h5_obj, data, include_channels
