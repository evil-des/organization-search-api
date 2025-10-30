from sqlalchemy.ext.asyncio import create_async_engine

from db.settings import database_settings

async_engine = create_async_engine(database_settings.async_url)
