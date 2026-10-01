from src.domain.global_exception import GlobalException
from http import HTTPStatus

class TrackNotFoundException(GlobalException):
    def __init__(
        self,
        message = "Track not Found"
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.NOT_FOUND
        )