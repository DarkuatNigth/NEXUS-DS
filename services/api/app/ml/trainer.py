import io
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from app.core.config import settings
from app.infra.cloud_client import cloud_client
from app.ml.preprocessing import clean_total_charges, TARGET
from app.ml.pipeline import build_pipeline
from app.repository.model_repository import save_model
from app.repository.metrics_repository import save_metrics

logger = logging.getLogger(__name__)


def train() -> dict:
    """
    Ciclo completo de entrenamiento:
    1. Descarga CSV desde S3
    2. Limpia TotalCharges
    3. Divide en train/test
    4. Entrena sklearn Pipeline
    5. Calcula métricas
    6. Guarda pipeline en S3 y métricas en SSM
    Retorna el dict de métricas.
    """
    logger.info("=== Inicio de entrenamiento ===")

    # 1. Descargar CSV desde S3
    csv_bytes = cloud_client.download_s3(settings.s3_csv_key)
    df = pd.read_csv(io.BytesIO(csv_bytes))
    logger.info("Dataset cargado: %d filas, %d columnas", len(df), len(df.columns))

    # 2. Limpiar TotalCharges (string con espacios → float, vacíos → NaN)
    df = clean_total_charges(df)

    # 3. Preparar X e y
    y = (df[TARGET].str.strip().str.lower() == "yes").astype(int)
    X = df.drop(columns=[TARGET, "customerID"], errors="ignore")

    # 4. Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5. Entrenar Pipeline completo (preprocesador + clasificador)
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    logger.info("Pipeline entrenado")

    # 6. Métricas
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "auc_roc": round(float(roc_auc_score(y_test, y_proba)), 4),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
    }
    logger.info("Métricas: %s", metrics)

    # 7. Persistir
    save_model(pipeline)
    save_metrics(metrics)

    logger.info("=== Entrenamiento completado ===")
    return metrics
