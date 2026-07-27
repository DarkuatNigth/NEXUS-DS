from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


SAMPLE_PAYLOAD = {
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "Yes",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 65.0,
    "TotalCharges": 780.0,
}


def test_health_endpoint():
    with patch("app.service.health_service.cloud_client") as mock_cc:
        mock_cc._s3.list_buckets.return_value = {"Buckets": []}
        from app.main import app

        with TestClient(app) as client:
            resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_predict_endpoint_returns_churn_and_probability():
    mock_pipeline = MagicMock()
    mock_pipeline.predict_proba.return_value = [[0.3, 0.7]]

    with (
        patch("app.service.model_service._pipeline", mock_pipeline),
        patch("app.router.predict.predict") as mock_predict,
    ):
        mock_predict.return_value = ("Yes", 0.7)
        from app.main import app

        with TestClient(app) as client:
            resp = client.post("/api/v1/predict", json=SAMPLE_PAYLOAD)

    assert resp.status_code == 200
    data = resp.json()
    assert "churn" in data
    assert "probability" in data
    assert data["churn"] in ("Yes", "No")
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_endpoint_409_when_no_model():
    with patch("app.router.predict.predict") as mock_predict:
        mock_predict.side_effect = ValueError("Modelo no entrenado.")
        from app.main import app

        with TestClient(app) as client:
            resp = client.post("/api/v1/predict", json=SAMPLE_PAYLOAD)

    assert resp.status_code == 409


def test_metrics_endpoint_404_when_no_metrics():
    with patch("app.service.metrics_service.load_metrics", return_value=None):
        from app.main import app

        with TestClient(app) as client:
            resp = client.get("/api/v1/metrics")

    assert resp.status_code == 404


def test_metrics_endpoint_returns_metrics():
    mock_metrics = {
        "accuracy": 0.85,
        "precision": 0.80,
        "recall": 0.75,
        "f1": 0.77,
        "auc_roc": 0.90,
        "train_samples": 5000,
        "test_samples": 1000,
    }
    with patch("app.service.metrics_service.load_metrics", return_value=mock_metrics):
        from app.main import app

        with TestClient(app) as client:
            resp = client.get("/api/v1/metrics")

    assert resp.status_code == 200
    data = resp.json()
    assert data["accuracy"] == 0.85
    assert data["auc_roc"] == 0.90


def test_train_endpoint_returns_202():
    with patch("app.router.train.launch_training", return_value=True):
        from app.main import app

        with TestClient(app) as client:
            resp = client.post("/api/v1/train")

    assert resp.status_code == 202


def test_train_endpoint_409_when_already_running():
    with patch("app.router.train.launch_training", return_value=False):
        from app.main import app

        with TestClient(app) as client:
            resp = client.post("/api/v1/train")

    assert resp.status_code == 409
