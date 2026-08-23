from src.domain.global_exception import GlobalException
from http import HTTPStatus

class InvalidScoreException(GlobalException):
    def __init__(
            self,
            message="Score must be between 0.5 and 5.0, in steps of 0.5"
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST
        )