import logging
import threading
from app.ml.trainer import train
from app.service.model_service import invalidate_pipeline

logger = logging.getLogger(__name__)

_train_state = {"status": "idle", "message": ""}
_lock = threading.Lock()


def get_status() -> dict:
    with _lock:
        return dict(_train_state)


def _run_training():
    with _lock:
        _train_state["status"] = "running"
        _train_state["message"] = "Entrenamiento en progreso..."
    try:
        metrics = train()
        invalidate_pipeline()
        with _lock:
            _train_state["status"] = "done"
            _train_state["message"] = f"Completado. Accuracy: {metrics['accuracy']}"
        logger.info("Entrenamiento completado: %s", metrics)
    except Exception as e:
        with _lock:
            _train_state["status"] = "failed"
            _train_state["message"] = str(e)
        logger.error("Error en entrenamiento: %s", e, exc_info=True)


def launch_training():
    with _lock:
        if _train_state["status"] == "running":
            return False  # ya hay un entrenamiento en curso
        _train_state["status"] = "running"
        _train_state["message"] = "Iniciando..."
    thread = threading.Thread(target=_run_training, daemon=True)
    thread.start()
    return True
