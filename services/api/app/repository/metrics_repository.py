import json
import logging

from app.core.config import settings
from app.infra.cloud_client import cloud_client

logger = logging.getLogger(__name__)


def save_metrics(metrics: dict) -> None:
    cloud_client.put_ssm(settings.ssm_metrics_path, json.dumps(metrics))
    logger.info("Métricas guardadas en SSM: %s", settings.ssm_metrics_path)


def load_metrics() -> dict | None:
    value = cloud_client.get_ssm(settings.ssm_metrics_path)
    if value is None:
        return None
    return json.loads(value)
