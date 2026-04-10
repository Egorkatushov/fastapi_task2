# src/core/exceptions/base.py
from enum import Enum
from typing import Optional, Any


class ErrorCode(str, Enum):
    """Коды ошибок для API"""
    # Общие ошибки
    INTERNAL_ERROR = "internal_error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    BAD_REQUEST = "bad_request"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"


class BaseDomainException(Exception):
    """Базовое исключение доменного слоя"""

    def __init__(self, detail: str, code: str = ErrorCode.BAD_REQUEST):
        self.detail = detail
        self.code = code
        super().__init__(detail)

    def get_detail(self) -> str:
        return self.detail

    def get_code(self) -> str:
        return self.code


class BaseDatabaseException(Exception):
    """Базовое исключение слоя БД"""

    def __init__(self, detail: str | None = None, code: str = ErrorCode.INTERNAL_ERROR):
        self.detail = detail or "Ошибка базы данных"
        self.code = code
        super().__init__(self.detail)

    def get_detail(self) -> str:
        return self.detail

    def get_code(self) -> str:
        return self.code


class AppException(Exception):
    """Базовое исключение приложения"""

    def __init__(
            self,
            message: str,
            code: str = ErrorCode.INTERNAL_ERROR,
            details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)