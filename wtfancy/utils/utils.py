import os
import numpy as np
from contextlib import contextmanager
import logging


def exactly_one_specified(*inputs):
    """
    Returns True if exactly one of *inputs is None

    Args:
        *inputs: One or more arguments to test against

    Returns:
        bool
    """
    not_none = np.array(list(map(lambda x: x is not None, inputs)))
    return np.sum(not_none) == 1

def create_folders(folders, create_deep=False):
    def safe_make(path, make_func):
        try:
            make_func(path)
        except FileExistsError:
            # If running many jobs in parallel this may occur
            pass
    make_func = os.mkdir if not create_deep else os.makedirs
    if isinstance(folders, str):
        if not os.path.exists(folders):
            safe_make(folders, make_func)
    else:
        folders = list(folders)
        for f in folders:
            if f is None:
                continue
            if not os.path.exists(f):
                safe_make(f, make_func)


def ensure_list_or_tuple(obj):
    """
    Takes some object and wraps it in a list - i.e. [obj] - unless the object
    is already a list or a tuple instance. In that case, simply returns 'obj'

    Args:
        obj: Any object

    Returns:
        [obj] if obj is not a list or tuple, else obj
    """
    return [obj] if not isinstance(obj, (list, tuple)) else obj


@contextmanager
def mne_no_log_context():
    """ Disables the (logger) of the mne module inside the context only """
    log = logging.getLogger('mne')
    mem = log.disabled
    log.disabled = True
    try:
        yield
    finally:
        log.disabled = mem