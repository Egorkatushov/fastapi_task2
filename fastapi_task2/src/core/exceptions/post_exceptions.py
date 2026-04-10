# src/core/exceptions/post_exceptions.py
from .base import BaseDomainException, ErrorCode


# ============ Domain исключения ============
class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class PostAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' уже существует"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)  # Используем CONFLICT


class PostAuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с ID='{author_id}' не найден"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class PostCategoryNotFoundException(BaseDomainException):
    _exception_text_template = "Категория с ID='{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        detail = self._exception_text_template.format(category_id=category_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class PostLocationNotFoundException(BaseDomainException):
    _exception_text_template = "Локация с ID='{location_id}' не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class PostTitleEmptyException(BaseDomainException):
    _exception_text_template = "Заголовок поста не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class PostTextEmptyException(BaseDomainException):
    _exception_text_template = "Содержание поста не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class PostTitleTooLongException(BaseDomainException):
    _exception_text_template = "Заголовок поста не может превышать {max_length} символов"

    def __init__(self, max_length: int = 256) -> None:
        detail = self._exception_text_template.format(max_length=max_length)
        super().__init__(detail=detail, code=ErrorCode.VALIDATION_ERROR)

class PostAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' уже существует"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)