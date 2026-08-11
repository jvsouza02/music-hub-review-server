from fastapi import Response

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"

def _set_cookies(
        response: Response,
        key: str,
        value: str,
        max_age: int
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite=True,
        max_age=max_age,
    )


def set_access_cookie(
        response: Response,
        token: str,
        max_age: int = 1800
) -> None:
    _set_cookies(response, ACCESS_TOKEN_KEY, f"Bearer {token}", max_age)


def refresh_access_cookie(
        response: Response,
        token: str,
        max_age: int = 604800
) -> None:
    _set_cookies(response, REFRESH_TOKEN_KEY, token, max_age)


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=ACCESS_TOKEN_KEY)
    response.delete_cookie(key=REFRESH_TOKEN_KEY)