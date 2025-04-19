from fastapi import APIRouter, Depends, Query
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.stat import StatCreate, StatOut, SavedStatAnalysisOut
from app.crud import stat as stat_crud
from datetime import datetime
from typing import List
from app.tasks.stat import run_stat_analysis
from app.utils.device import ensure_device_exists
from app.utils.validators import validate_date_range
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.post("/", response_model=StatOut)
async def add_stat(
    stat_in: StatCreate,
    db: AsyncSession = Depends(get_session)
):
    return await stat_crud.create_stat(db, stat_in)

@router.get("/{device_id}", response_model=List[StatOut])
async def get_stats(
    device_id: int,
    start: datetime = Query(None),
    end: datetime = Query(None),
    db: AsyncSession = Depends(get_session)
):
    await ensure_device_exists(db, device_id)
    validate_date_range(start, end)
    return await stat_crud.get_stats_for_device(db, device_id, start, end)

from app.schemas.stat import StatAnalysisOut

@router.get("/analysis/{device_id}", response_model=StatAnalysisOut)
async def analyze_stats(
    device_id: int,
    start: datetime = Query(None),
    end: datetime = Query(None),
    db: AsyncSession = Depends(get_session)
):
    await ensure_device_exists(db, device_id)
    validate_date_range(start, end)
    return await stat_crud.analyze_device_stats(db, device_id, start, end)


@router.post("/analysis/{device_id}/async")
async def trigger_analysis(device_id: int, start: datetime = None, end: datetime = None, db: AsyncSession = Depends(get_session)):
    logger.info("Отправляем задачу Celery run_stat_analysis")
    await ensure_device_exists(db, device_id)
    validate_date_range(start, end)
    run_stat_analysis.delay(device_id, start.isoformat() if start else None, end.isoformat() if end else None)
    return {"status": "Задача передана на фоновую обработку"}


@router.get("/analysis/result/{device_id}", response_model=List[SavedStatAnalysisOut])
async def get_saved_analysis_results(
    device_id: int,
    db: AsyncSession = Depends(get_session)
):
    return await stat_crud.get_saved_analysis_for_device(db, device_id)
