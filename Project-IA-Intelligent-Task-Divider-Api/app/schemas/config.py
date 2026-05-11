# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import List, Dict, Union, Optional, Any

class ConfigResponse(BaseModel):
    columnas_requeridas: List[str]
    columnas_numericas: List[str]
    columnas_categoricas: List[str]
    columnas_outlier_iqr: List[str]
    tipos_esperados: Dict[str, str]
    rangos_validos: Dict[str, Any]
    riesgo_label: Dict[str, str]
    rf_params: Dict[str, List[Any]]
    gb_params: Dict[str, List[Any]]
    kfold_splits: int
    random_state: int
    test_size: float
    n_iter_search: int

class ConfigUpdate(BaseModel):
    kfold_splits: Optional[int] = None
    random_state: Optional[int] = None
    test_size: Optional[float] = None
    n_iter_search: Optional[int] = None
