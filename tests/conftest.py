from unittest.mock import patch

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws


@pytest.fixture(scope="function")
def aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")


@pytest.fixture(scope="function")
def moto_s3(aws_credentials):
    with mock_aws():
        client = boto3.client(
            "s3",
            endpoint_url=None,  # moto intercepta sin endpoint real
            region_name="us-east-1",
        )
        client.create_bucket(Bucket="nexus-ds-bucket")
        yield client


@pytest.fixture(scope="function")
def moto_ssm(aws_credentials):
    with mock_aws():
        client = boto3.client(
            "ssm",
            endpoint_url=None,
            region_name="us-east-1",
        )
        yield client


@pytest.fixture(scope="function")
def mock_cloud_client():
    """Mock del CloudClient para tests de API sin boto3."""
    with patch("app.infra.cloud_client.cloud_client") as mock_client:
        yield mock_client


@pytest.fixture(scope="function")
def test_client(mock_cloud_client):
    """TestClient de FastAPI con CloudClient mockeado."""
    from app.main import app

    with TestClient(app) as client:
        yield client
