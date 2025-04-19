from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, func
from app.db.base import Base

class StatAnalysisResult(Base):
    __tablename__ = "stat_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    start = Column(DateTime(timezone=True), nullable=True)
    end = Column(DateTime(timezone=True), nullable=True)

    x = Column(JSON, nullable=False)
    y = Column(JSON, nullable=False)
    z = Column(JSON, nullable=False)
