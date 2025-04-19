import asyncio
from app.db.session import engine
from app.db.base import Base
import app.models.device
import app.models.stat
import app.models.stat_analysis_results
from app.models.device import Device
from app.models.stat import Stat
from app.models.stat_analysis_results import StatAnalysisResult

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Device.__table__.create)
        await conn.run_sync(Stat.__table__.create)
        await conn.run_sync(StatAnalysisResult.__table__.create)
    print(" Таблицы успешно созданы")

if __name__ == "__main__":
    asyncio.run(init_models())
