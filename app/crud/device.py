from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.device import Device
from app.schemas.device import DeviceCreate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def create_device(db: AsyncSession, device_in: DeviceCreate) -> Device:
    try:
        device = Device(**device_in.dict())
        db.add(device)
        await db.commit()
        await db.refresh(device)
        return device
    except Exception as e:
        logger.exception("Ошибка при создании устройства")
        raise HTTPException(status_code=500, detail="Ошибка сервера при создании устройства")

async def get_device(db: AsyncSession, device_id: int) -> Device:
    result = await db.execute(select(Device).where(Device.id == device_id))
    return result.scalar_one_or_none()
