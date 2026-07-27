import numpy as np
import pandas as pd
from app.ml.preprocessing import (
    NUMERIC_FEATURES,
    TARGET,
    build_column_transformer,
    clean_total_charges,
)


def _make_sample_df(n: int = 10) -> pd.DataFrame:
    """DataFrame sintético con el mismo esquema que Telco."""
    return pd.DataFrame(
        {
            "customerID": [f"id-{i}" for i in range(n)],
            "gender": ["Male", "Female"] * (n // 2),
            "SeniorCitizen": [0, 1] * (n // 2),
            "Partner": ["Yes", "No"] * (n // 2),
            "Dependents": ["Yes", "No"] * (n // 2),
            "tenure": list(range(n)),
            "PhoneService": ["Yes"] * n,
            "MultipleLines": ["No phone service"] * n,
            "InternetService": ["DSL", "Fiber optic"] * (n // 2),
            "OnlineSecurity": ["Yes", "No internet service"] * (n // 2),
            "OnlineBackup": ["Yes", "No"] * (n // 2),
            "DeviceProtection": ["No", "Yes"] * (n // 2),
            "TechSupport": ["No internet service", "Yes"] * (n // 2),
            "StreamingTV": ["Yes", "No"] * (n // 2),
            "StreamingMovies": ["No", "Yes"] * (n // 2),
            "Contract": ["Month-to-month", "One year"] * (n // 2),
            "PaperlessBilling": ["Yes", "No"] * (n // 2),
            "PaymentMethod": ["Electronic check", "Mailed check"] * (n // 2),
            "MonthlyCharges": [50.0 + i for i in range(n)],
            "TotalCharges": ["600.0", " ", "800.0", "900.5", " "] * (n // 5),
            "Churn": ["Yes", "No"] * (n // 2),
        }
    )


def test_clean_total_charges_converts_spaces_to_nan():
    df = _make_sample_df(10)
    cleaned = clean_total_charges(df)
    assert cleaned["TotalCharges"].dtype == float
    # Los espacios " " deben convertirse a NaN
    assert cleaned["TotalCharges"].isna().sum() > 0


def test_clean_total_charges_does_not_modify_original():
    df = _make_sample_df(10)
    _ = clean_total_charges(df)
    # Original sin modificar (deep copy)
    assert df["TotalCharges"].dtype == object


def test_build_column_transformer_output_shape():
    df = _make_sample_df(20)
    df = clean_total_charges(df)
    X = df.drop(columns=[TARGET, "customerID"])
    ct = build_column_transformer()
    result = ct.fit_transform(X)
    # Filas = n; columnas > len(NUMERIC_FEATURES) por OHE
    assert result.shape[0] == 20
    assert result.shape[1] > len(NUMERIC_FEATURES)


def test_build_column_transformer_handles_nan_in_numeric():
    """El SimpleImputer debe manejar NaN en TotalCharges sin crash."""
    df = _make_sample_df(10)
    df = clean_total_charges(df)
    X = df.drop(columns=[TARGET, "customerID"])
    ct = build_column_transformer()
    result = ct.fit_transform(X)
    assert not np.isnan(result).any()
