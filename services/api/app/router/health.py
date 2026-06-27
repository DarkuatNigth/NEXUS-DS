from fastapi import APIRouter
from app.infra.cloud_client import cloud_client
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
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
