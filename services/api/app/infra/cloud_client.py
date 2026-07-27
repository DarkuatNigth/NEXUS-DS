import io
import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)


class CloudClient:
    def __init__(self):
        kwargs = dict(
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        self._s3 = boto3.client("s3", **kwargs)
        self._ssm = boto3.client("ssm", **kwargs)

    # ── S3 ──────────────────────────────────────────────────────────────────

    def upload_s3(self, key: str, data: bytes, bucket: str | None = None) -> None:
        bucket = bucket or settings.s3_bucket
        self._s3.put_object(Bucket=bucket, Key=key, Body=data)
        logger.info("S3 upload: s3://%s/%s (%d bytes)", bucket, key, len(data))

    def download_s3(self, key: str, bucket: str | None = None) -> bytes:
        bucket = bucket or settings.s3_bucket
        resp = self._s3.get_object(Bucket=bucket, Key=key)
        data = resp["Body"].read()
        logger.info("S3 download: s3://%s/%s (%d bytes)", bucket, key, len(data))
        return data

    def exists_s3(self, key: str, bucket: str | None = None) -> bool:
        bucket = bucket or settings.s3_bucket
        try:
            self._s3.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] in ("404", "NoSuchKey"):
                return False
            raise

    def create_bucket_if_not_exists(self, bucket: str | None = None) -> None:
        bucket = bucket or settings.s3_bucket
        try:
            self._s3.head_bucket(Bucket=bucket)
            logger.info("S3 bucket '%s' already exists", bucket)
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ("404", "NoSuchBucket"):
                self._s3.create_bucket(Bucket=bucket)
                logger.info("S3 bucket '%s' created", bucket)
            else:
                raise

    # ── SSM ─────────────────────────────────────────────────────────────────

    def put_ssm(self, name: str, value: str) -> None:
        self._ssm.put_parameter(Name=name, Value=value, Type="String", Overwrite=True)
        logger.info("SSM put: %s", name)

    def get_ssm(self, name: str) -> str | None:
        try:
            resp = self._ssm.get_parameter(Name=name)
            return resp["Parameter"]["Value"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "ParameterNotFound":
                return None
            raise


# Instancia singleton del cliente
cloud_client = CloudClient()
