class BasePythonSchemaError(Exception):
    """Base class in order to catch all python-schema easily (if needed)
    """


class PayloadError(BasePythonSchemaError):
    pass


class ValueNotSetError(PayloadError):
    """Happens when we try to read a field that was never loaded
    """


class NormalisationError(PayloadError):
    """Base error for all the normalisation issues
    """

    def __init__(self, message, *args, **kwargs):
        self.errors = [message]

        super().__init__(message, *args, **kwargs)


class NoneNotAllowedError(NormalisationError):
    """Happens when we try to load field with None, but it's not allowed
    """


class ValidationError(PayloadError):
    """Exception happens when one or more of validators fails.
    """
    def __init__(self, errors, *args, **kwargs):
        self.errors = errors

        super().__init__(*args, **kwargs)
