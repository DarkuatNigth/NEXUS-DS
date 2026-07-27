import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Mapeo de nombres del dataset IBM extendido (33 col, nombres con espacios)
# al dataset estándar Kaggle (21 col, camelCase). pandas rename ignora claves ausentes,
# por lo que el mapeo es seguro para ambos formatos.
_COLUMN_ALIASES: dict[str, str] = {
    "CustomerID": "customerID",
    "Gender": "gender",
    "Senior Citizen": "SeniorCitizen",
    "Tenure Months": "tenure",
    "Phone Service": "PhoneService",
    "Multiple Lines": "MultipleLines",
    "Internet Service": "InternetService",
    "Online Security": "OnlineSecurity",
    "Online Backup": "OnlineBackup",
    "Device Protection": "DeviceProtection",
    "Tech Support": "TechSupport",
    "Streaming TV": "StreamingTV",
    "Streaming Movies": "StreamingMovies",
    "Paperless Billing": "PaperlessBilling",
    "Payment Method": "PaymentMethod",
    "Monthly Charges": "MonthlyCharges",
    "Total Charges": "TotalCharges",
    "Churn Label": "Churn",
}

NUMERIC_FEATURES = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL_FEATURES = [
    "Contract",
    "PaymentMethod",
    "InternetService",
    "OnlineSecurity",
    "TechSupport",
    "OnlineBackup",
    "DeviceProtection",
    "StreamingTV",
    "StreamingMovies",
    "MultipleLines",
    "PhoneService",
    "PaperlessBilling",
    "gender",
    "Partner",
    "Dependents",
    "SeniorCitizen",
]
TARGET = "Churn"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renombra columnas del dataset IBM extendido (33 col) al esquema estándar.
    Si el dataset ya usa nombres estándar (21 col), no modifica nada."""
    return df.rename(columns=_COLUMN_ALIASES)


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    TotalCharges viene como string con espacios vacíos en algunos registros.
    Esta función DEBE llamarse ANTES de construir el ColumnTransformer.
    """
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def build_column_transformer() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
