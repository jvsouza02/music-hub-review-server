from fastapi import HTTPException, status, Request
from src.infrastructure.cache.redis_client import RedisClient

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        
        # Script Lua 100% Atômico: Executa direto no motor C do Redis
        self.lua_script = """
        local current = redis.call('INCR', KEYS[1])
        if current == 1 then
            redis.call('EXPIRE', KEYS[1], ARGV[1])
        end
        if current > tonumber(ARGV[2]) then
            return 0
        end
        return 1
        """

    async def __call__(self, request: Request):
        redis = RedisClient().client
        
        # Pegamos o IP para não bloquear rotas públicas (como cadastro de usuário)
        client_ip = request.client.host if request.client else "127.0.0.1"
        cache_key = f"rate_limit:{client_ip}:{request.url.path}"

        # Executa o script atomicamente (impossível haver falha de concorrência)
        is_allowed = await redis.eval(
            self.lua_script,
            1,                     # Quantidade de chaves (KEYS)
            cache_key,             # Mapeia para KEYS[1]
            self.window_seconds,   # Mapeia para ARGV[1]
            self.max_requests      # Mapeia para ARGV[2]
        )

        if is_allowed == 0:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit excedido. Máximo de {self.max_requests} requisições a cada {self.window_seconds} segundos."
            )