"""
Script de inicialización de la infraestructura cloud en Floci.
Crea el bucket S3 y sube el dataset si no existe en S3.
El formato del dataset (xlsx, csv, etc.) se determina por S3_DATASET_KEY en .env.
"""
import logging
import sys
from pathlib import Path
from app.core.logging import setup_logging
from app.core.config import settings
from app.infra.cloud_client import cloud_client

setup_logging()
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("=== NEXUS-DS init_cloud ===")

    # 1. Crear bucket S3
    cloud_client.create_bucket_if_not_exists()

    # 2. Subir dataset si no existe en S3
    if cloud_client.exists_s3(settings.s3_dataset_key):
        logger.info("Dataset ya existe en S3: %s — saltando subida", settings.s3_dataset_key)
    else:
        # El nombre del archivo se deriva de S3_DATASET_KEY en .env
        filename = Path(settings.s3_dataset_key).name
        local_file = Path("/app/data/raw") / filename
        if not local_file.exists():
            logger.error(
                "Archivo no encontrado en %s. "
                "Coloca el dataset en data/raw/%s antes de correr nexus-init.",
                local_file,
                filename,
            )
            sys.exit(1)
        data = local_file.read_bytes()
        cloud_client.upload_s3(settings.s3_dataset_key, data)
        logger.info("Dataset subido a S3: %s (%d bytes)", settings.s3_dataset_key, len(data))

    logger.info("=== init_cloud completado ===")


if __name__ == "__main__":
    main()
