import io
import logging

import joblib

from app.core.config import settings
from app.infra.cloud_client import cloud_client

logger = logging.getLogger(__name__)


def save_model(pipeline) -> None:
    buffer = io.BytesIO()
    joblib.dump(pipeline, buffer)
    buffer.seek(0)
    cloud_client.upload_s3(settings.s3_model_key, buffer.read())
    logger.info("Modelo guardado en S3: %s", settings.s3_model_key)


def load_model():
    data = cloud_client.download_s3(settings.s3_model_key)
    pipeline = joblib.load(io.BytesIO(data))
    logger.info("Modelo cargado desde S3: %s", settings.s3_model_key)
    return pipeline


def model_exists() -> bool:
    return cloud_client.exists_s3(settings.s3_model_key)
