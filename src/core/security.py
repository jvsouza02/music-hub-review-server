from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from .config import settings
encode_value: str = settings.model_config['env_file_encoding'] 


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw( # -> Checa se as senhas são iguais
        password.encode(encode_value),
        hashed_password.encode(encode_value)
    )


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(encode_value), salt)
    return hashed.decode(encode_value)


def _create_token(
        data: dict,
        expires_delta: timedelta,
        token_type: str
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_access_token(data: dict):
    delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(data, delta, "access")


def refresh_access_token(data: dict):
    delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(data, delta, "refresh")


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )