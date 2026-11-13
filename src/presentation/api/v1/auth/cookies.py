from fastapi import Response

from src.core.config import settings

from .constants import ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY


def _set_cookies(
    response: Response,
    key: str,
    value: str,
    max_age: int,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=max_age,
    )


def set_access_cookie(
    response: Response,
    token: str,
    max_age: int | None = None,
) -> None:
    effective_max_age = (
        settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        if max_age is None
        else max_age
    )

    _set_cookies(
        response,
        ACCESS_TOKEN_KEY,
        f"Bearer {token}",
        effective_max_age,
    )


def refresh_access_cookie(
    response: Response,
    token: str,
    max_age: int | None = None,
) -> None:
    effective_max_age = (
        settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        if max_age is None
        else max_age
    )

    _set_cookies(
        response,
        REFRESH_TOKEN_KEY,
        token,
        effective_max_age,
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(
        key=ACCESS_TOKEN_KEY,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )

    response.delete_cookie(
        key=REFRESH_TOKEN_KEY,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )