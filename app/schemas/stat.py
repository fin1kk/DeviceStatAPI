from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class StatCreate(BaseModel):
    device_id: int
    x: float = Field(..., ge=-1000, le=1000)
    y: float = Field(..., ge=-1000, le=1000)
    z: float = Field(..., ge=-1000, le=1000)

class StatOut(BaseModel):
    id: int
    device_id: int
    x: float = Field(..., ge=-1000, le=1000)
    y: float = Field(..., ge=-1000, le=1000)
    z: float = Field(..., ge=-1000, le=1000)
    timestamp: datetime

    class Config:
        orm_mode = True

class AxisStats(BaseModel):
    min: float
    max: float
    sum: float
    count: int
    median: float

class StatAnalysisOut(BaseModel):
    x: AxisStats
    y: AxisStats
    z: AxisStats

class SavedStatAnalysisOut(BaseModel):
    id: int
    device_id: int
    start: Optional[datetime]
    end: Optional[datetime]
    x: Dict[str, float]
    y: Dict[str, float]
    z: Dict[str, float]

    class Config:
        orm_mode = True