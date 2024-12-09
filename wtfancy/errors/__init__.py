"""
Small collection of custom objects.
Sometimes used for their custom names only.
"""


class CouldNotLoadError(ResourceWarning):
    def __init__(self, *args, study_id=None):
        super(CouldNotLoadError, self).__init__(*args)
        self.study_id = study_id


class ChannelNotFoundError(CouldNotLoadError):
    def __init__(self, *args, **kwargs):
        super(ChannelNotFoundError, self).__init__(*args, **kwargs)


class H5ChannelRootError(KeyError): pass


class H5VariableAttributesError(ValueError): pass


class MissingHeaderFieldError(KeyError): pass


class HeaderFieldTypeError(TypeError): pass


class LengthZeroSignalError(ValueError): pass


