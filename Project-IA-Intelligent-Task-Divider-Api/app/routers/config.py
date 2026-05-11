# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.schemas.config import ConfigResponse, ConfigUpdate
from app.services.config_service import config_service

router = APIRouter()

@router.get("/config", response_model=ConfigResponse)
def get_config():
    return config_service.get_config()

@router.put("/config", response_model=ConfigResponse)
def update_config(request: ConfigUpdate):
    data = request.model_dump(exclude_unset=True) if hasattr(request, "model_dump") else request.dict(exclude_unset=True)
    return config_service.update_config(data)
