# src/core/exceptions/category_exceptions.py
from .base import BaseDomainException, ErrorCode


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class CategoryAlreadyExistsException(BaseDomainException):  # ← ДОБАВЬТЕ
    _exception_text_template = "Категория с ID='{category_id}' уже существует"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class CategoryNameAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Категория с названием '{name}' уже существует"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class CategoryNameEmptyException(BaseDomainException):
    _exception_text_template = "Название категории не может быть пустым"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)