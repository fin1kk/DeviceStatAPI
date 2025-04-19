from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.device import DeviceCreate, DeviceOut
from app.crud import device as device_crud
from app.db.session import get_session

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=DeviceOut)
async def create_device(
    device_in: DeviceCreate,
    db: AsyncSession = Depends(get_session)
):
    return await device_crud.create_device(db, device_in)
