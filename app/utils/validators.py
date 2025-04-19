from datetime import datetime
from fastapi import HTTPException

def validate_date_range(start: datetime = None, end: datetime = None):
    if start and end and start > end:
        raise HTTPException(
            status_code=400,
            detail="Начальная дата не может быть позже конечной"
        )
