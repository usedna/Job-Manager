class Error(Exception):
    pass


class InvalidFormatError(Error):
    """Raise when the file format isn't supported by opencv"""
    pass


class InvalidInputError(Error):
    pass


class OutOfRangeError(Error):
    pass


class IsNegativeException(Error):
    pass
