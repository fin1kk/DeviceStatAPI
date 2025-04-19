from app.core.celery_config import celery_app
from app.db.sync_session import SyncSessionLocal, sync_engine
from app.crud.stat import analyze_device_stats
from app.models.stat_analysis_results import StatAnalysisResult
from app.utils.validators import validate_date_range
from datetime import datetime
import logging
from sqlalchemy import inspect

logger = logging.getLogger(__name__)
print(f"[Celery] Подключение к БД: {sync_engine.url}")
print(f"[Celery] Таблицы в БД: {inspect(sync_engine).get_table_names()}")

@celery_app.task
def run_stat_analysis(device_id: int, start: str = None, end: str = None):
    logger.info(f"[Celery] Таблицы в БД: {inspect(sync_engine).get_table_names()}")
    logger.info("Задач Celery начала выполняться")
    
    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None
    validate_date_range(start_dt, end_dt)

    from app.crud.stat import analyze_device_stats_sync
    
    try:
        with SyncSessionLocal() as session:
            result = analyze_device_stats_sync(session, device_id, start_dt, end_dt)
            analysis = StatAnalysisResult(
                device_id=device_id,
                start=start_dt,
                end=end_dt,
                x=result["x"],
                y=result["y"],
                z=result["z"],
            )
            session.add(analysis)
            #logger.info(f"[Celery] Таблицы в БД: {inspect(sync_engine).get_table_names()}")
            session.commit()
    except Exception as e:
        logger.exception("Ошибка при анализе статистики")