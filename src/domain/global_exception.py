from http import HTTPStatus

class GlobalException(Exception):
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)