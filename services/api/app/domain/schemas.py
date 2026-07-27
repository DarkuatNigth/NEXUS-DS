from typing import Literal

from pydantic import BaseModel


class PredictRequest(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: int  # 0 o 1
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    ]
    MonthlyCharges: float
    TotalCharges: float


class PredictResponse(BaseModel):
    churn: Literal["Yes", "No"]
    probability: float  # 0.0 a 1.0


class TrainStatus(BaseModel):
    status: Literal["idle", "running", "done", "failed"]
    message: str = ""


class MetricsResponse(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1: float
    auc_roc: float
    train_samples: int
    test_samples: int
