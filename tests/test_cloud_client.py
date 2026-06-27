import io
import json
import pytest
import boto3
from moto import mock_aws
from unittest.mock import patch, MagicMock


@mock_aws
def test_upload_and_download_s3():
    """upload_s3 sube bytes; download_s3 recupera los mismos bytes."""
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="nexus-ds-bucket")

    with patch("app.infra.cloud_client.boto3") as mock_boto3:
        mock_boto3.client.return_value = s3
        # Reimportar con moto activo
        from app.infra.cloud_client import CloudClient
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.aws_endpoint_url = "http://localhost:4566"
            mock_settings.aws_access_key_id = "test"
            mock_settings.aws_secret_access_key = "test"
            mock_settings.aws_region = "us-east-1"
            mock_settings.s3_bucket = "nexus-ds-bucket"

            client = CloudClient.__new__(CloudClient)
            client._s3 = s3
            client._ssm = MagicMock()

            data = b"hello nexus-ds"
            client.upload_s3("test/file.txt", data, bucket="nexus-ds-bucket")
            result = client.download_s3("test/file.txt", bucket="nexus-ds-bucket")
            assert result == data


@mock_aws
def test_exists_s3_true_and_false():
    """exists_s3 retorna True si la key existe, False si no."""
    import boto3
    from app.infra.cloud_client import CloudClient
    from botocore.exceptions import ClientError

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="nexus-ds-bucket")
    s3.put_object(Bucket="nexus-ds-bucket", Key="exists.txt", Body=b"x")

    client = CloudClient.__new__(CloudClient)
    client._s3 = s3
    client._ssm = MagicMock()

    assert client.exists_s3("exists.txt", bucket="nexus-ds-bucket") is True
    assert client.exists_s3("not_there.txt", bucket="nexus-ds-bucket") is False


@mock_aws
def test_put_and_get_ssm():
    """put_ssm guarda un valor; get_ssm lo recupera correctamente."""
    import boto3
    from app.infra.cloud_client import CloudClient

    ssm = boto3.client("ssm", region_name="us-east-1")

    client = CloudClient.__new__(CloudClient)
    client._s3 = MagicMock()
    client._ssm = ssm

    client.put_ssm("/nexus-ds/test/param", "hello-value")
    result = client.get_ssm("/nexus-ds/test/param")
    assert result == "hello-value"


@mock_aws
def test_get_ssm_not_found():
    """get_ssm retorna None si el parámetro no existe."""
    import boto3
    from app.infra.cloud_client import CloudClient

    ssm = boto3.client("ssm", region_name="us-east-1")

    client = CloudClient.__new__(CloudClient)
    client._s3 = MagicMock()
    client._ssm = ssm

    result = client.get_ssm("/nexus-ds/nonexistent")
    assert result is None
