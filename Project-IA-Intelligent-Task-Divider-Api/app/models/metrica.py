from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class MetricaModelo(Base):
    __tablename__ = "metricas_modelo"

    id = Column(Integer, primary_key=True, index=True)
    
    # Ganadores
    ganador_tasks = Column(String(50), nullable=False)
    ganador_time = Column(String(50), nullable=False)
    ganador_risk = Column(String(50), nullable=False)
    
    # Regresión: sub-tareas
    tasks_mae = Column(Float, nullable=True)
    tasks_rmse = Column(Float, nullable=True)
    tasks_mape = Column(Float, nullable=True)
    tasks_r2 = Column(Float, nullable=True)
    
    # Regresión: tiempo
    time_mae = Column(Float, nullable=True)
    time_rmse = Column(Float, nullable=True)
    time_mape = Column(Float, nullable=True)
    time_r2 = Column(Float, nullable=True)
    
    # Clasificación: riesgo
    risk_accuracy = Column(Float, nullable=True)
    risk_f1 = Column(Float, nullable=True)
    risk_precision = Column(Float, nullable=True)
    risk_recall = Column(Float, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
