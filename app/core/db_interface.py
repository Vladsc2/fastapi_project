from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import config


class DataBaseInterface():
    def __init__(self, url: str, echo: bool = False):

        self.engine = create_async_engine(
            url=url,
            echo=echo
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session




db_interface = DataBaseInterface(
    url=config.db_url,
    echo=config.db_echo
)