# src/core/exceptions/location_exceptions.py
from .base import BaseDomainException, ErrorCode


# ============ Domain исключения ============
class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация с ID='{location_id}' не найдена"

    def __init__(self, location_id: int) -> None:
        detail = self._exception_text_template.format(location_id=location_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class LocationNameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Локация с названием='{name}' уже существует"

    def __init__(self, name: str) -> None:
        detail = self._exception_text_template.format(name=name)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class LocationNameEmptyException(BaseDomainException):
    _exception_text_template = "Название локации не может быть пустым или состоять только из пробелов"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template, code=ErrorCode.VALIDATION_ERROR)


class LocationNameTooLongException(BaseDomainException):
    _exception_text_template = "Название локации не может превышать {max_length} символов"

    def __init__(self, max_length: int = 256) -> None:
        detail = self._exception_text_template.format(max_length=max_length)
        super().__init__(detail=detail, code=ErrorCode.VALIDATION_ERROR)