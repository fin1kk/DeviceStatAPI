from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.stat import Stat
from app.schemas.stat import StatCreate
from datetime import datetime
from typing import List
from statistics import median
from app.models.stat_analysis_results import StatAnalysisResult

from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

async def create_stat(db: AsyncSession, stat: StatCreate):
    try:
        db_stat = Stat(**stat.dict())
        db.add(db_stat)
        await db.commit()
        await db.refresh(db_stat)
        return db_stat
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Invalid device_id: does not exist")


async def get_stats_for_device(
    db: AsyncSession,
    device_id: int,
    start: datetime = None,
    end: datetime = None
) -> List[Stat]:
    stmt = select(Stat).where(Stat.device_id == device_id)
    if start:
        stmt = stmt.where(Stat.timestamp >= start)
    if end:
        stmt = stmt.where(Stat.timestamp <= end)
    result = await db.execute(stmt)
    return result.scalars().all()


async def analyze_device_stats(
    db: AsyncSession,
    device_id: int,
    start: datetime = None,
    end: datetime = None
):
    stmt = select(Stat).where(Stat.device_id == device_id)
    if start:
        stmt = stmt.where(Stat.timestamp >= start)
    if end:
        stmt = stmt.where(Stat.timestamp <= end)
    result = await db.execute(stmt)
    stats = result.scalars().all()

    return _analyze_stat_list(stats)


def analyze_device_stats_sync(
    db: Session,
    devicee_id: int,
    start: datetime = None,
    end: datetime = None
):
    stmt = select(Stat).where(Stat.device_id == devicee_id)
    if start:
        stmt = stmt.where(Stat.timestamp >= start)
    if end:
        stmt = stmt.where(Stat.timestamp <= end)
    result = db.execute(stmt)
    stats = result.scalars().all()

    return _analyze_stat_list(stats)


def _analyze_stat_list(stats: List[Stat]):
    def analyze_axis(values):
        if not values:
            return {"min": 0, "max": 0, "sum": 0, "count": 0, "median": 0}
        return {
            "min": min(values),
            "max": max(values),
            "sum": sum(values),
            "count": len(values),
            "median": median(values),
        }

    x_vals = [s.x for s in stats]
    y_vals = [s.y for s in stats]
    z_vals = [s.z for s in stats]

    return {
        "x": analyze_axis(x_vals),
        "y": analyze_axis(y_vals),
        "z": analyze_axis(z_vals),
    }

async def get_saved_analysis_for_device(
    db: AsyncSession,
    device_id: int
) -> List[StatAnalysisResult]:
    stmt = select(StatAnalysisResult).where(StatAnalysisResult.device_id == device_id)
    result = await db.execute(stmt)
    return result.scalars().all()