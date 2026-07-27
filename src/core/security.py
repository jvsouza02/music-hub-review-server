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
    salt = bcrypt.gensalt() # -> Gera um 'salt' aleatório para montar a senha hasheada
    hashed = bcrypt.hashpw(password.encode(encode_value), salt) # -> Cria a senha hasheada com a senha e o salt gerado
    return hashed.decode(encode_value) # Retorna a senha hasheada decodificada em formato de string 


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy() # -> Copia os dados

    # -> Verifica se o tempo delta foi passado, caso sim, ele é utilizado, caso contrário, o tempo será gerado com a função 'timedelta'
    #    passando o tempo definido nas variáveis de ambiente
    if (expires_delta): 
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire}) # -> Atualiza os dados passando o tempo de expiração do token

    # Encodifica o jwt
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt