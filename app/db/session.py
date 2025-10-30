from sqlalchemy.ext.asyncio import async_sessionmaker

from db.base import async_engine

Session = async_sessionmaker(async_engine)


async def get_session():
    async with Session() as session:
        yield session
