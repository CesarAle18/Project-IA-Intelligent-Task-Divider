# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import Literal, Tuple, Dict, List
from datetime import datetime

class PrediccionRequest(BaseModel):
    sp: float = Field(..., gt=0, description="Story Points del proyecto")
    experiencia: int = Field(..., ge=1, le=3, description="Nivel del equipo (1=junior, 2=mid, 3=senior)")
    rendimiento: float = Field(..., ge=0.0, le=1.0, description="Velocidad del equipo entre 0.0 y 1.0")
    complejidad: float = Field(..., ge=1.0, description="Nivel de complejidad técnica")
    dependencias: float = Field(..., ge=0.0, description="Número de dependencias externas")
    tipo_tarea: Literal["Backend", "Frontend", "DevOps", "Diseño", "QA"]
    urgencia: Literal["Baja", "Media", "Alta"]

class PrediccionResponse(BaseModel):
    id: int
    pred_tasks: int
    ci_tasks: Tuple[float, float]
    pred_time: int
    ci_time: Tuple[float, float]
    pred_risk: str
    probas: Dict[str, float]
    created_at: datetime

    class Config:
        from_attributes = True

class PrediccionListResponse(BaseModel):
    id: int
    sp: float
    tipo_tarea: str
    urgencia: str
    pred_tasks: int
    pred_time: int
    pred_risk: str
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[PrediccionListResponse]
    total: int
    page: int
    per_page: int
    pages: int
