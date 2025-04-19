from pydantic import BaseModel

class DeviceCreate(BaseModel):
    name: str

class DeviceOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
