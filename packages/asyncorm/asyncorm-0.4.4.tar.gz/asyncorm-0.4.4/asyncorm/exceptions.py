__all__ = (
    "AsyncormException",
    "FieldError",
    "ModelDoesNotExist",
    "ModelError",
    "AppError",
    "MultipleObjectsReturned",
    "QuerysetError",
    "SerializerError",
    "ConfigError",
    "CommandError",
    "MigrationError",
)


class AsyncormException(Exception):
    pass


class CommandError(AsyncormException):
    """Exceptions to be raised when command errors"""

    pass


class FieldError(AsyncormException):
    """to be raised when there are field errors detected"""

    pass


class ModelError(AsyncormException):
    """to be raised when there are model errors detected"""

    pass


class QuerysetError(AsyncormException):
    """to be raised when there are queryset errors detected"""

    pass


class ConfigError(AsyncormException):
    """to be raised when there are configuration errors detected"""

    pass


class MigrationError(AsyncormException):
    """to be raised when there are configuration errors detected"""

    pass


class ModelDoesNotExist(AsyncormException):
    """to be raised when there are model errors detected"""

    pass


class MultipleObjectsReturned(AsyncormException):
    """to be raised when there are model errors detected"""

    pass


class SerializerError(AsyncormException):
    """to be raised when there are model errors detected"""

    pass


class AppError(AsyncormException):
    """to be raised when there are class App or config errors detected"""

    pass
