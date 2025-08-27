from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True) # get the database and create an engine

SessionLocal = sessionmaker(
    bind=engine,  # to read from the database
    class_=AsyncSession, # to use async sessions
    expire_on_commit=False, # to not expire the session after commit, save state in cache no need to query again
)

# from now on if the model class inherits from Base, it will be mapped to a database table
# create a declarative base class to define the database models
Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session