from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MetricaResponse(BaseModel):
    id: int
    ganador_tasks: str
    ganador_time: str
    ganador_risk: str
    
    tasks_mae: Optional[float]
    tasks_rmse: Optional[float]
    tasks_mape: Optional[float]
    tasks_r2: Optional[float]
    
    time_mae: Optional[float]
    time_rmse: Optional[float]
    time_mape: Optional[float]
    time_r2: Optional[float]
    
    risk_accuracy: Optional[float]
    risk_f1: Optional[float]
    risk_precision: Optional[float]
    risk_recall: Optional[float]
    
    created_at: datetime

    class Config:
        from_attributes = True
