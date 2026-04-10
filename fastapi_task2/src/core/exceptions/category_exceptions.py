# src/core/exceptions/category_exceptions.py
from .base import BaseDomainException, ErrorCode


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class CategoryAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' уже существует"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class CategoryNameAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Категория с названием '{name}' уже существует"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class CategoryTitleEmptyException(BaseDomainException):
    _exception_text_template = "Название категории не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class CategoryDescriptionEmptyException(BaseDomainException):
    _exception_text_template = "Описание категории не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class CategorySlugEmptyException(BaseDomainException):
    _exception_text_template = "Slug категории не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)