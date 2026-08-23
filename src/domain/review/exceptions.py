from src.domain.global_exception import GlobalException
from http import HTTPStatus

class ReviewNotFoundException(GlobalException):
    def __init__(
        self,
        message="Review not found"
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.NOT_FOUND
        )

class ReviewAlreadyExistsException(GlobalException):
    def __init__(
        self,
        message="Review already exists"
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.CONFLICT
        )

class ReviewPermissionDeniedException(GlobalException):
    def __init__(
        self,
        message="Permission denied"
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.FORBIDDEN
        )    