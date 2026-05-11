import os
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from app.schemas.prediccion import PrediccionRequest

class MLService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.is_loaded = False
        self.pipe_tasks = None
        self.pipe_time = None
        self.pipe_risk = None
        self.meta = {}
        self.models_dir = os.getenv("MODELS_DIR", "./models")

    def load_models(self) -> bool:
        try:
            self.pipe_tasks = joblib.load(os.path.join(self.models_dir, "pipe_tasks.pkl"))
            self.pipe_time = joblib.load(os.path.join(self.models_dir, "pipe_time.pkl"))
            self.pipe_risk = joblib.load(os.path.join(self.models_dir, "pipe_risk.pkl"))
            
            with open(os.path.join(self.models_dir, "meta.json"), "r") as f:
                self.meta = json.load(f)
                
            self.is_loaded = True
            print("✅ Modelos cargados correctamente.")
            return True
        except FileNotFoundError as e:
            print(f"⚠️ Error cargando modelos: {e}. Asegúrate de exportar los .pkl a {self.models_dir}")
            self.is_loaded = False
            return False

    def _intervalo_confianza_bootstrap(self, pipe, X_input: pd.DataFrame, ci: float = 0.90) -> Tuple[float, float]:
        modelo = pipe.named_steps["model"]
        if hasattr(modelo, "estimators_"):
            preprocesador = pipe.named_steps["preprocesador"]
            X_trans = preprocesador.transform(X_input)
            preds = np.array([est.predict(X_trans)[0] for est in modelo.estimators_])
            alpha = (1 - ci) / 2
            return float(np.percentile(preds, alpha * 100)), float(np.percentile(preds, (1 - alpha) * 100))
        else:
            pred = pipe.predict(X_input)[0]
            return float(pred * 0.85), float(pred * 1.15)

    def predict(self, req: PrediccionRequest) -> Dict[str, Any]:
        if not self.is_loaded:
            raise RuntimeError("Los modelos no están cargados.")

        # Create DataFrame from input
        features = ["SP", "Experiencia", "Rendimiento", "Complejidad", "Dependencias", "TipoTarea", "Urgencia"]
        X_input = pd.DataFrame([[
            req.sp, req.experiencia, req.rendimiento, req.complejidad, req.dependencias, req.tipo_tarea, req.urgencia
        ]], columns=features)

        # Predict tasks
        pred_tasks_raw = self.pipe_tasks.predict(X_input)[0]
        pred_tasks = max(1, int(round(pred_tasks_raw)))
        ci_tasks = self._intervalo_confianza_bootstrap(self.pipe_tasks, X_input)

        # Predict time
        pred_time_raw = self.pipe_time.predict(X_input)[0]
        pred_time = max(1, int(round(pred_time_raw)))
        ci_time = self._intervalo_confianza_bootstrap(self.pipe_time, X_input)

        # Predict risk
        pred_risk_idx = int(self.pipe_risk.predict(X_input)[0])
        riesgo_label = {"0": "ALTO", "1": "MEDIO", "2": "BAJO"}
        pred_risk_label = riesgo_label.get(str(pred_risk_idx), "DESCONOCIDO")

        # Probabilities
        probas = {}
        if hasattr(self.pipe_risk.named_steps["model"], "predict_proba"):
            proba_array = self.pipe_risk.predict_proba(X_input)[0]
            clases = self.pipe_risk.classes_
            probas = {riesgo_label.get(str(int(c)), str(c)): round(float(p) * 100, 1) for c, p in zip(clases, proba_array)}

        return {
            "pred_tasks": pred_tasks,
            "ci_tasks": ci_tasks,
            "pred_time": pred_time,
            "ci_time": ci_time,
            "pred_risk": pred_risk_label,
            "probas": probas
        }

ml_service = MLService()
