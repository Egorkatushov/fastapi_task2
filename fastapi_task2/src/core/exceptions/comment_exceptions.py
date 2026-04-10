# src/core/exceptions/comment_exceptions.py
from .base import BaseDomainException, ErrorCode


# ============ Domain исключения ============
class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с ID='{comment_id}' не найден"

    def __init__(self, comment_id: int) -> None:
        detail = self._exception_text_template.format(comment_id=comment_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class CommentAlreadyExistsException(BaseDomainException):  # ← ДОБАВЬТЕ ЭТОТ КЛАСС
    _exception_text_template = "Комментарий с ID='{comment_id}' уже существует"

    def __init__(self, comment_id: int) -> None:
        detail = self._exception_text_template.format(comment_id=comment_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class CommentAuthorNotFoundException(BaseDomainException):
    _exception_text_template = "Автор с ID='{author_id}' не найден"

    def __init__(self, author_id: int) -> None:
        detail = self._exception_text_template.format(author_id=author_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class CommentPostNotFoundException(BaseDomainException):
    _exception_text_template = "Пост с ID='{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        detail = self._exception_text_template.format(post_id=post_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class CommentTextEmptyException(BaseDomainException):
    _exception_text_template = "Текст комментария не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class CommentTextTooLongException(BaseDomainException):
    _exception_text_template = "Текст комментария не может превышать {max_length} символов"

    def __init__(self, max_length: int = 1000) -> None:
        detail = self._exception_text_template.format(max_length=max_length)
        super().__init__(detail=detail, code=ErrorCode.VALIDATION_ERROR)