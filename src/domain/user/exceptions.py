from src.domain.global_exception import GlobalException
from http import HTTPStatus

class EmailAlreadyInUseException(GlobalException):
    def __init__(self, message="Este email já está em uso."):
        super().__init__(message=message, status_code=HTTPStatus.BAD_REQUEST)

class UserNotFoundException(GlobalException):
    def __init__(self, message="User not found."):
        super().__init__(message=message, status_code=HTTPStatus.NOT_FOUND)

class InvalidPasswordException(GlobalException):
    def __init__(self, message="Invalid password"):
        super().__init__(message=message, status_code=HTTPStatus.UNAUTHORIZED)