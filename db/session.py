from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

DB_URL = os.getenv("DB_URL")

engine = create_async_engine(url=DB_URL, echo=False)
session_factory = async_sessionmaker(engine)
