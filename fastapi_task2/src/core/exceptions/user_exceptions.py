from .base import BaseDomainException, ErrorCode


class UserAlreadyExistsException(BaseDomainException):
    _exception_text_template = "Пользователь с ID='{user_id}' уже существует"

    def __init__(self, user_id: int) -> None:
        detail = self._exception_text_template.format(user_id=user_id)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)

class UserNotFoundByLoginException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' не найден"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с username='{username}' не найден"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с ID='{user_id}' не найден"

    def __init__(self, user_id: int) -> None:
        detail = self._exception_text_template.format(user_id=user_id)
        super().__init__(detail=detail, code=ErrorCode.NOT_FOUND)


class UserLoginIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с логином='{login}' уже существует"

    def __init__(self, login: str) -> None:
        detail = self._exception_text_template.format(login=login)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с username='{username}' уже существует"

    def __init__(self, username: str) -> None:
        detail = self._exception_text_template.format(username=username)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с email='{email}' уже существует"

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail, code=ErrorCode.CONFLICT)


class UserPasswordTooWeakException(BaseDomainException):
    _exception_text_template = "Пароль слишком слабый: {reason}"

    def __init__(self, reason: str) -> None:
        detail = self._exception_text_template.format(reason=reason)
        super().__init__(detail=detail, code=ErrorCode.VALIDATION_ERROR)


class UserInvalidEmailException(BaseDomainException):
    _exception_text_template = "Некорректный email: '{email}'"

    def __init__(self, email: str) -> None:
        detail = self._exception_text_template.format(email=email)
        super().__init__(detail=detail, code=ErrorCode.VALIDATION_ERROR)