from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from math import ceil

from app.database import get_db
from app.models.prediccion import Prediccion
from app.schemas.prediccion import PrediccionRequest, PrediccionResponse, PaginatedResponse
from app.services.ml_service import ml_service

router = APIRouter()

@router.post("/predecir", response_model=PrediccionResponse)
def predecir(request: PrediccionRequest, db: Session = Depends(get_db)):
    if not ml_service.is_loaded:
        raise HTTPException(status_code=503, detail="Los modelos ML no están cargados en el servidor.")

    try:
        resultado = ml_service.predict(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Guardar en base de datos
    db_prediccion = Prediccion(
        sp=request.sp,
        experiencia=request.experiencia,
        rendimiento=request.rendimiento,
        complejidad=request.complejidad,
        dependencias=request.dependencias,
        tipo_tarea=request.tipo_tarea,
        urgencia=request.urgencia,
        pred_tasks=resultado["pred_tasks"],
        ci_tasks_lower=resultado["ci_tasks"][0],
        ci_tasks_upper=resultado["ci_tasks"][1],
        pred_time=resultado["pred_time"],
        ci_time_lower=resultado["ci_time"][0],
        ci_time_upper=resultado["ci_time"][1],
        pred_risk=resultado["pred_risk"],
        proba_alto=resultado["probas"].get("ALTO"),
        proba_medio=resultado["probas"].get("MEDIO"),
        proba_bajo=resultado["probas"].get("BAJO")
    )
    
    db.add(db_prediccion)
    db.commit()
    db.refresh(db_prediccion)
    
    return {
        "id": db_prediccion.id,
        "pred_tasks": db_prediccion.pred_tasks,
        "ci_tasks": (db_prediccion.ci_tasks_lower, db_prediccion.ci_tasks_upper),
        "pred_time": db_prediccion.pred_time,
        "ci_time": (db_prediccion.ci_time_lower, db_prediccion.ci_time_upper),
        "pred_risk": db_prediccion.pred_risk,
        "probas": {k: v for k, v in [
            ("ALTO", db_prediccion.proba_alto),
            ("MEDIO", db_prediccion.proba_medio),
            ("BAJO", db_prediccion.proba_bajo)
        ] if v is not None},
        "created_at": db_prediccion.created_at
    }

@router.get("/historial", response_model=PaginatedResponse)
def get_historial(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    total = db.query(Prediccion).count()
    items = db.query(Prediccion).order_by(Prediccion.id.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": ceil(total / per_page) if total > 0 else 0
    }

@router.get("/historial/{id}", response_model=PrediccionResponse)
def get_prediccion(id: int, db: Session = Depends(get_db)):
    pred = db.query(Prediccion).filter(Prediccion.id == id).first()
    if not pred:
        raise HTTPException(status_code=404, detail="Predicción no encontrada")
        
    return {
        "id": pred.id,
        "pred_tasks": pred.pred_tasks,
        "ci_tasks": (pred.ci_tasks_lower, pred.ci_tasks_upper),
        "pred_time": pred.pred_time,
        "ci_time": (pred.ci_time_lower, pred.ci_time_upper),
        "pred_risk": pred.pred_risk,
        "probas": {k: v for k, v in [
            ("ALTO", pred.proba_alto),
            ("MEDIO", pred.proba_medio),
            ("BAJO", pred.proba_bajo)
        ] if v is not None},
        "created_at": pred.created_at
    }
