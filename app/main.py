from fastapi import FastAPI
from app.api.V1.routers import stat, device
import app.core.logging_config

app = FastAPI(title="Device Stat API")

app.include_router(stat.router)
app.include_router(device.router)
