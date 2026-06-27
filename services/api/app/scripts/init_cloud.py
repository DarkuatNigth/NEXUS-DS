"""
Script de inicialización de la infraestructura cloud en Floci.
Crea el bucket S3 y sube el CSV de Telco si no existe en S3.
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

    # 2. Subir CSV si no existe en S3
    if cloud_client.exists_s3(settings.s3_csv_key):
        logger.info("CSV ya existe en S3: %s — saltando subida", settings.s3_csv_key)
    else:
        # El CSV debe estar en /app/data/raw/ (montado vía bind mount o copiado)
        local_csv = Path("/app/data/raw/Telco_customer_churn.csv")
        if not local_csv.exists():
            logger.error(
                "CSV no encontrado en %s. "
                "Coloca el dataset en data/raw/Telco_customer_churn.csv antes de correr nexus-init.",
                local_csv,
            )
            sys.exit(1)
        data = local_csv.read_bytes()
        cloud_client.upload_s3(settings.s3_csv_key, data)
        logger.info("CSV subido a S3: %s (%d bytes)", settings.s3_csv_key, len(data))

    logger.info("=== init_cloud completado ===")

if __name__ == "__main__":
    main()
