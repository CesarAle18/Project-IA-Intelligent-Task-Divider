from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import prediccion, metricas, config
from app.services.ml_service import ml_service

app = FastAPI(
    title="IA Task Divider API",
    description="API de predicción inteligente para división de tareas de software",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    # Cargar modelos .pkl
    ml_service.load_models()

app.include_router(prediccion.router, tags=["Predicción"])
app.include_router(metricas.router, tags=["Métricas"])
app.include_router(config.router, tags=["Configuración"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "models_loaded": ml_service.is_loaded}
