import pytest
import pandas as pd
from app.ml.preprocessing import clean_total_charges, TARGET
from app.ml.pipeline import build_pipeline


def _make_training_df(n: int = 50) -> pd.DataFrame:
    """DataFrame sintético mínimo para entrenar el pipeline."""
    import numpy as np
    rng = np.random.default_rng(42)
    n_half = n // 2
    return pd.DataFrame({
        "customerID": [f"id-{i}" for i in range(n)],
        "gender": ["Male", "Female"] * n_half,
        "SeniorCitizen": [0, 1] * n_half,
        "Partner": ["Yes", "No"] * n_half,
        "Dependents": ["Yes", "No"] * n_half,
        "tenure": list(range(n)),
        "PhoneService": ["Yes"] * n,
        "MultipleLines": ["No phone service"] * n,
        "InternetService": ["DSL", "Fiber optic"] * n_half,
        "OnlineSecurity": ["Yes", "No internet service"] * n_half,
        "OnlineBackup": ["Yes", "No"] * n_half,
        "DeviceProtection": ["No", "Yes"] * n_half,
        "TechSupport": ["No internet service", "Yes"] * n_half,
        "StreamingTV": ["Yes", "No"] * n_half,
        "StreamingMovies": ["No", "Yes"] * n_half,
        "Contract": ["Month-to-month", "One year"] * n_half,
        "PaperlessBilling": ["Yes", "No"] * n_half,
        "PaymentMethod": ["Electronic check", "Mailed check"] * n_half,
        "MonthlyCharges": rng.uniform(20, 120, n).tolist(),
        "TotalCharges": [str(v) if i % 5 != 0 else " " for i, v in
                         enumerate(rng.uniform(100, 5000, n).tolist())],
        "Churn": ["Yes", "No"] * n_half,
    })


def test_pipeline_fit_predict():
    """El pipeline completo entrena y produce predicciones sin error."""
    df = _make_training_df(50)
    df = clean_total_charges(df)
    y = (df[TARGET].str.strip().str.lower() == "yes").astype(int)
    X = df.drop(columns=[TARGET, "customerID"])

    pipeline = build_pipeline(n_estimators=10, random_state=0)
    pipeline.fit(X, y)
    preds = pipeline.predict(X)
    assert len(preds) == len(X)
    assert set(preds).issubset({0, 1})


def test_pipeline_predict_proba():
    """predict_proba retorna probabilidades en [0, 1] con shape correcto."""
    df = _make_training_df(50)
    df = clean_total_charges(df)
    y = (df[TARGET].str.strip().str.lower() == "yes").astype(int)
    X = df.drop(columns=[TARGET, "customerID"])

    pipeline = build_pipeline(n_estimators=10, random_state=0)
    pipeline.fit(X, y)
    probas = pipeline.predict_proba(X)
    assert probas.shape == (len(X), 2)
    assert (probas >= 0).all() and (probas <= 1).all()
