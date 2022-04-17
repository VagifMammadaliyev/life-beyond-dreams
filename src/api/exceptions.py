from typing import Any, Dict, Optional


class APIError(Exception):
    def __init__(
        self, status_code: int, detail: str, error_data: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_data = error_data


class ForbiddenError(APIError):
    def __init__(
        self,
        status_code: Optional[int] = 403,
        detail: Optional[str] = "Forbidden",
        error_data: Optional[Dict[str, Any]] = None,
    ):
        super().__int__(status_code, detail, error_data)


class ServerError(APIError):
    def __init__(
        self,
        status_code: Optional[int] = 500,
        detail: Optional[str] = "Some unwanted error",
        error_data: Optional[Dict[str, Any]] = None,
    ):
        super().__int__(status_code, detail, error_data)


class ClientError(APIError):
    def __init__(
        self,
        status_code: Optional[int] = 400,
        detail: Optional[str] = "Invalid request",
        error_data: Optional[Dict[str, Any]] = None,
    ):
        super().__int__(status_code, detail, error_data)
