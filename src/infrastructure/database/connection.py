from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings

# engine = create_async_engine(settings.DATABASE_URL)
engine = create_async_engine(
    "sqlite+aiosqlite:///./database.db",
    connect_args={"check_same_thread": False} # Apenas para sqlite
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db