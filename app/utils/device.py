from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.device import get_device

async def ensure_device_exists(session: AsyncSession, device_id: int):
    device = await get_device(session, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
    return device
