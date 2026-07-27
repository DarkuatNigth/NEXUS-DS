import logging

from app.repository.metrics_repository import load_metrics

logger = logging.getLogger(__name__)


def get_metrics() -> dict | None:
    return load_metrics()
