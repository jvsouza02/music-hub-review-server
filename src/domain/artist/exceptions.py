from src.domain.global_exception import GlobalException
from http import HTTPStatus

class ArtistNotFoundException(GlobalException):
    def __init__(self, message="Artist not found."):
        super().__init__(message=message, status_code=HTTPStatus.NOT_FOUND)
