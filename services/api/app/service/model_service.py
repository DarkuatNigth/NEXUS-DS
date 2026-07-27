import logging

import pandas as pd

from app.repository.model_repository import load_model, model_exists

logger = logging.getLogger(__name__)

_pipeline = None


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        if not model_exists():
            return None
        _pipeline = load_model()
        logger.info("Pipeline cargado en memoria (lazy)")
    return _pipeline


def invalidate_pipeline():
    global _pipeline
    _pipeline = None
    logger.info("Singleton del pipeline invalidado — se recargará en el siguiente predict")


def predict(data: dict) -> tuple[str, float]:
    pipeline = get_pipeline()
    if pipeline is None:
        raise ValueError("Modelo no entrenado. Ejecuta POST /api/v1/train primero.")
    df = pd.DataFrame([data])
    proba = pipeline.predict_proba(df)[0, 1]
    label = "Yes" if proba >= 0.5 else "No"
    return label, float(proba)
