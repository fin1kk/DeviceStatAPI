from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, func
from app.db.base import Base

class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())
