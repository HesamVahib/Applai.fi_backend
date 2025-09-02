import asyncio
from database import engine, Base
from models.models import Jobs

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())