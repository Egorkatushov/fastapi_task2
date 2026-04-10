# src/core/exceptions/database_exceptions.py
from .base import BaseDatabaseException, ErrorCode


# ============ Общие ошибки БД ============
class DatabaseOperationError(BaseDatabaseException):
    """Общая ошибка операции с БД"""
    pass


class DatabaseConnectionError(BaseDatabaseException):
    """Ошибка подключения к БД"""

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            detail=detail or "Не удалось подключиться к базе данных",
            code=ErrorCode.INTERNAL_ERROR
        )


class DatabaseIntegrityError(BaseDatabaseException):
    """Ошибка целостности данных в БД"""
    pass


# ============ Исключения для пользователей (БД) ============
class UserNotFoundExceptionDB(BaseDatabaseException):
    pass


class UserAlreadyExistsExceptionDB(BaseDatabaseException):
    pass


# ============ Исключения для постов (БД) ============
class PostNotFoundExceptionDB(BaseDatabaseException):
    pass


class PostAuthorNotFoundExceptionDB(BaseDatabaseException):
    pass


class PostCategoryNotFoundExceptionDB(BaseDatabaseException):
    pass


class PostLocationNotFoundExceptionDB(BaseDatabaseException):
    pass


# ============ Исключения для комментариев (БД) ============
class CommentNotFoundExceptionDB(BaseDatabaseException):
    pass


class CommentAuthorNotFoundExceptionDB(BaseDatabaseException):
    pass


class CommentPostNotFoundExceptionDB(BaseDatabaseException):
    pass


class CommentIntegrityErrorDB(BaseDatabaseException):
    pass


# ============ Исключения для локаций (БД) ============
class LocationNotFoundExceptionDB(BaseDatabaseException):
    pass


class LocationAlreadyExistsExceptionDB(BaseDatabaseException):
    pass


# ============ Исключения для категорий (БД) ============
class CategoryNotFoundExceptionDB(BaseDatabaseException):
    pass


class CategoryAlreadyExistsExceptionDB(BaseDatabaseException):
    pass