from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from app.ml.preprocessing import build_column_transformer


def build_pipeline(n_estimators: int = 100, random_state: int = 42) -> Pipeline:
    return Pipeline(
        [
            ("preprocessor", build_column_transformer()),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=n_estimators,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )
