# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, Float, String, DateTime
# pyrefly: ignore [missing-import]
from sqlalchemy.sql import func
from app.database import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    
    # Inputs
    sp = Column(Float, nullable=False)
    experiencia = Column(Integer, nullable=False)
    rendimiento = Column(Float, nullable=False)
    complejidad = Column(Float, nullable=False)
    dependencias = Column(Float, nullable=False)
    tipo_tarea = Column(String(20), nullable=False, index=True)
    urgencia = Column(String(10), nullable=False)
    
    # Outputs
    pred_tasks = Column(Integer, nullable=False)
    ci_tasks_lower = Column(Float, nullable=True)
    ci_tasks_upper = Column(Float, nullable=True)
    pred_time = Column(Integer, nullable=False)
    ci_time_lower = Column(Float, nullable=True)
    ci_time_upper = Column(Float, nullable=True)
    pred_risk = Column(String(10), nullable=False)
    proba_alto = Column(Float, nullable=True)
    proba_medio = Column(Float, nullable=True)
    proba_bajo = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now(), index=True)
