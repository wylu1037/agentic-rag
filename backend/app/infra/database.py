from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings

_engine = None
_session_factory = None


def init_engine(settings: Settings) -> None:
    global _engine, _session_factory
    _engine = create_async_engine(settings.database_url, echo=False, pool_size=5, max_overflow=10)
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)


async def dispose_engine() -> None:
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None


async def get_session() -> AsyncSession:
    if _session_factory is None:
        raise RuntimeError("Database engine not initialized. Call init_engine() first.")
    async with _session_factory() as session:
        yield session
