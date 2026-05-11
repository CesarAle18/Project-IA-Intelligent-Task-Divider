# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List
import os
import pandas as pd
from app.database import get_db
from app.models.metrica import MetricaModelo
from app.schemas.metrica import MetricaResponse

router = APIRouter()

def load_legacy_metrics(db: Session):
    count = db.query(MetricaModelo).count()
    if count > 0:
        return
        
    csv_path = os.getenv("METRICS_CSV_PATH", "./data/metricas_historial.csv")
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                m = MetricaModelo(
                    ganador_tasks=str(row.get("ganador_tasks", "")),
                    ganador_time=str(row.get("ganador_time", "")),
                    ganador_risk=str(row.get("ganador_risk", "")),
                    tasks_mae=float(row.get("tasks_MAE", 0)) if pd.notnull(row.get("tasks_MAE")) else None,
                    tasks_rmse=float(row.get("tasks_RMSE", 0)) if pd.notnull(row.get("tasks_RMSE")) else None,
                    tasks_mape=float(row.get("tasks_MAPE", 0)) if pd.notnull(row.get("tasks_MAPE")) else None,
                    tasks_r2=float(row.get("tasks_R2", 0)) if pd.notnull(row.get("tasks_R2")) else None,
                    time_mae=float(row.get("time_MAE", 0)) if pd.notnull(row.get("time_MAE")) else None,
                    time_rmse=float(row.get("time_RMSE", 0)) if pd.notnull(row.get("time_RMSE")) else None,
                    time_mape=float(row.get("time_MAPE", 0)) if pd.notnull(row.get("time_MAPE")) else None,
                    time_r2=float(row.get("time_R2", 0)) if pd.notnull(row.get("time_R2")) else None,
                    risk_accuracy=float(row.get("risk_Accuracy", 0)) if pd.notnull(row.get("risk_Accuracy")) else None,
                    risk_f1=float(row.get("risk_F1", 0)) if pd.notnull(row.get("risk_F1")) else None,
                    risk_precision=float(row.get("risk_Precision", 0)) if pd.notnull(row.get("risk_Precision")) else None,
                    risk_recall=float(row.get("risk_Recall", 0)) if pd.notnull(row.get("risk_Recall")) else None,
                )
                db.add(m)
            db.commit()
        except Exception as e:
            print(f"Error loading legacy metrics: {e}")

@router.get("/metricas", response_model=List[MetricaResponse])
def get_metricas(db: Session = Depends(get_db)):
    load_legacy_metrics(db)
    items = db.query(MetricaModelo).order_by(MetricaModelo.id.desc()).all()
    return items
