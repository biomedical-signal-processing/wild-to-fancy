"""
A set of functions for extracting header information from data objects
Typically only used internally in from wtfancy.io.header.header_extractors

Each function takes some data or header-like object and returns a dictionary with at least
the following keys:

{
    'n_channels': int,
    'channel_names': list of strings,
    'sample_rate': int
    'date': datetime or None
    'length': int
}

Note: length gives the number of samples, divide by sample_rate to get length_sec
"""

import numpy as np
import h5py
from datetime import datetime
from wtfancy.errors import (MissingHeaderFieldError, HeaderFieldTypeError,
                            LengthZeroSignalError, H5VariableAttributesError)


def _assert_header(header):
    """
    Checks that a standardized header:
        1) contains the right field names
        2) each value has an expected type
        3) the 'length' value is greater than 0
    Args:
        header: dict
    Returns: dict
    """
    field_requirements = [
        ("n_channels", [int]),
        ("channel_names", [list]),
        ("sample_rate", [int]),
        ("date", [datetime, type(None)]),
        ("length", [int])
    ]
    for field, valid_types in field_requirements:
        if field not in header:
            raise MissingHeaderFieldError(f"Missing value '{field}' from header '{header}'. "
                                          "This could be an error in the code implementation. "
                                          "Please raise this issue on GitHub.")
        type_ = type(header[field])
        if type_ not in valid_types:
            raise HeaderFieldTypeError(f"Field {field} of type {type_} was not expected, expected one of {valid_types}")
    if header['length'] <= 0:
        raise LengthZeroSignalError(f"Expected key 'length' to be a non-zero integer, "
                                    f"but header {header} has value {header['length']}")
    return header


def _standardized_edf_header(raw_edf):
    """
    Header extraction function for RawEDF and Raw objects.
    Reads the number of channels, channel names and sample rate properties
    If existing, reads the date information as well.

    Returns:
        Header information as dict
    """
    # Each tuple below follows the format:
    # 1) output name, 2) edf_obj name, 3) function to apply to the read
    # value, 4) whether a missing value should raise an error.
    header_map = [("n_channels", "nchan", int, True),
                  ("channel_names", "ch_names", list, True),
                  ("sample_rate", "sfreq", int, True),
                  ("date", "meas_date", datetime.utcfromtimestamp, False)]
    if isinstance(raw_edf.info["meas_date"], (tuple, list)):
        assert raw_edf.info["meas_date"][1] == 0
        raw_edf.info["meas_date"] = raw_edf.info["meas_date"][0]
    header = {}
    for renamed, org, transform, raise_err in header_map:
        value = raw_edf.info.get(org)
        try:
            value = transform(value)
        except Exception as e:
            if raise_err:
                raise HeaderFieldTypeError("Missing or invalid value in EDF file for key {} "
                                           "- got {}".format(org, value)) from e
        header[renamed] = value
    header["length"] = len(raw_edf)
    return _assert_header(header)


def _standardized_wfdb_header(wfdb_record):
    """
    Header extraction function for WFDB Record objects.
    Reads the number of channels, channel names and sample rate properties
    If existing, reads the date information as well.

    Returns:
        Header information as dict
    """
    # Each tuple below follows the format:
    # 1) output name, 2) record_obj name, 3) function to apply to the read
    # value, 4) whether a missing value should raise an error.
    header_map = [("n_channels", "n_sig", int, True),
                  ("channel_names", "sig_name", list, True),
                  ("sample_rate", "fs", int, True),
                  ("date", "base_date", datetime.utcfromtimestamp, False),
                  ("length", "sig_len", int, True)]
    header = {}
    for renamed, org, transform, raise_err in header_map:
        value = getattr(wfdb_record, org, None)
        try:
            value = transform(value)
        except Exception as e:
            if raise_err:
                raise HeaderFieldTypeError("Missing or invalid value in WFDB file for key {} "
                                           "- got {}".format(org, value)) from e
        header[renamed] = value
    return _assert_header(header)


def _traverse_h5_file(root_node, attributes=None):
    attributes = dict((attributes or {}))
    attributes.update(root_node.attrs)
    results = {}
    if isinstance(root_node, h5py.Dataset):
        # Leaf node
        attributes["length"] = len(root_node)
        results[root_node.name] = attributes
    else:
        for key in root_node:
            results.update(_traverse_h5_file(root_node[key], attributes))
    return results


def _get_unique_value(items):
    """
    Takes a list of items, checks that all are equal (in value, ==) and returns the unique value.
    Returns None if the list is empty.
    Raises ValueError if not all items are not equal.
    Args:
        items: List
    Returns:
        The unique item in list
    """
    if len(items) == 0:
        return None
    for item in items[1:]:
        if item != items[0]:
            raise H5VariableAttributesError(f"The input list '{items}' contains more than 1 unique value")
    return items[0]


def _standardized_h5_header(h5_file, channel_group_name="channels"):
    """
    Header extraction function for h5py.File objects.
    The object must:
      - Have an attribute 'sample_rate'
      - Have a group named {channel_group_name} which stores the data for all channels as
        Dataset entries under the group (can be nested in deeper groups too)
    Can have:
      - An attribute 'date' which gives a date string or unix timestamp integer

    Currently raises an error if any attribute in ('date', 'sample_rate', 'length') are not equal among all
    datasets in the archive.

    All attributes may be set at any node, and will affect any non-attributed node deeper in the tree.
    E.g. setting the 'sample_rate' attribute on the root note will have it affect all datasets, unless
    the attribute is set on deeper nodes too in which case the later will overwrite the root attribute for
    all its nested, un-attributed children.

    Returns:
        Header information as dict
    """
    # Traverse the h5 archive for datasets and assigned attributes
    h5_content = _traverse_h5_file(h5_file[channel_group_name], attributes=h5_file.attrs)
    header = {
        "channel_names": [],
        "channel_paths": {},  # will store channel_name: channel path entries
        "sample_rate": [],
        "date": [],
        "length": []
    }
    for channel_path, attributes in h5_content.items():
        channel_name = channel_path.split("/")[-1]
        header["channel_paths"][channel_name] = channel_path
        header["channel_names"].append(channel_name)
        header["sample_rate"].append(attributes.get("sample_rate"))
        header["date"].append(attributes.get("date"))
        header["length"].append(attributes.get("length"))
    header["n_channels"] = len(h5_content)

    # Ensure all dates, lengths and sample rate attributes are equal
    # TODO: Remove this restriction at least for sample rates; requires handling at data loading time
    try:
        header["date"] = _get_unique_value(header["date"])
        header["sample_rate"] = int(_get_unique_value(header["sample_rate"]))
        header["length"] = int(_get_unique_value(header["length"]))
    except H5VariableAttributesError as e:
        raise H5VariableAttributesError("Datasets stored in the specified H5 archive differ with respect to one or "
                                        "multiple of the following attributes: 'date', 'sampling_rate', 'length'. "
                                        "All datasets must currently match with respect to those attributes.") from e

    # Get datetime date or set to None
    date = header["date"]
    if not isinstance(date, str) and (isinstance(date, int) or np.issubdtype(date, np.integer)):
        date = datetime.utcfromtimestamp(date)
    elif not isinstance(date, datetime):
        date = None
    header["date"] = date
    return _assert_header(header)
