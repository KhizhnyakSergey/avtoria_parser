from typing import Any, Optional, Dict, Union


class BaseError(Exception):
    pass

class DetailedError(BaseError):
    url: Optional[str] = None

    def __init__(self, message: str, content: Union[str, Dict[str, Any]]) -> None:
        self.message = message
        self.content = content

    def __str__(self) -> str:
        message = self.message + f'\n{self.content}'
        if self.url:
            message += f"\n(background on this error at: {self.url})"
        return message

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"

class APIError(DetailedError):
    label: str = 'API server says'

    def __init__(
        self,
        status_code: int,
        content: Union[str, Dict[str, Any]],
        message: str = '',
    ) -> None:
        super().__init__(message=message, content=content)
        self.status_code = status_code

    def __str__(self) -> str:
        original_message = super().__str__()
        return f"{self.label} - {original_message}"

class ClientDecodeError(BaseError):
    def __init__(self, message: str, original: Exception, data: Any) -> None:
        self.message = message
        self.original = original
        self.data = data

    def __str__(self) -> str:
        original_type = type(self.original)
        return (
            f"{self.message}\n"
            f"Caused from error: "
            f"{original_type.__module__}.{original_type.__name__}: {self.original}\n"
            f"Content: {self.data}"
        )
    
class NetworkError(BaseError):
    pass

class BadRequestError(APIError):
    pass

class NotFoundError(APIError):
    pass

class ConflictError(APIError):
    pass

class UnauthorizedError(APIError):
    pass

class ForbiddenError(APIError):
    pass

class EntityTooLarge(APIError):
    pass

class ServerError(APIError):
    pass

class NotValidMethodError(BaseError):
    pass

class TooManyRequestsError(APIError):
    pass


