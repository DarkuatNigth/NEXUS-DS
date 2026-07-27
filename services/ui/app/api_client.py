import os

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_health() -> dict:
    resp = requests.get(f"{API_BASE_URL}/health", timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_metrics() -> dict | None:
    try:
        resp = requests.get(f"{API_BASE_URL}/api/v1/metrics", timeout=5)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def predict(payload: dict) -> dict:
    resp = requests.post(
        f"{API_BASE_URL}/api/v1/predict",
        json=payload,
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def trigger_train() -> dict:
    resp = requests.post(f"{API_BASE_URL}/api/v1/train", timeout=10)
    return resp.json()


def get_train_status() -> dict:
    resp = requests.get(f"{API_BASE_URL}/api/v1/train/status", timeout=5)
    resp.raise_for_status()
    return resp.json()
