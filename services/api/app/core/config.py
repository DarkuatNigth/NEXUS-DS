from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    aws_endpoint_url: str = "http://floci:4566"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"
    s3_bucket: str = "nexus-ds-bucket"
    s3_dataset_key: str = "raw/Telco_customer_churn.xlsx"
    s3_model_key: str = "models/pipeline.joblib"
    ssm_metrics_path: str = "/nexus-ds/metrics/latest"

settings = Settings()
