from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.router import health, train, predict, metrics

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # El modelo NO se precarga aquí — lazy loading en primer /predict
    yield


app = FastAPI(
    title="NEXUS-DS API",
    description="MLOps API para predicción de Telco Customer Churn",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(train.router)
app.include_router(predict.router)
app.include_router(metrics.router)
