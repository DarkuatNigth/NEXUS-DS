import logging

from app.core.config import settings
from app.infra.cloud_client import cloud_client

logger = logging.getLogger(__name__)


def check_health() -> dict:
    floci_ok = False
    try:
        cloud_client._s3.list_buckets()
        floci_ok = True
    except Exception:
        pass
    return {
        "status": "ok",
        "floci": "connected" if floci_ok else "unreachable",
        "endpoint": settings.aws_endpoint_url,
    }
