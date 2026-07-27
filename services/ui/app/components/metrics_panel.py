import streamlit as st

from app.api_client import get_metrics


def render_metrics_panel():
    st.sidebar.title("Modelo — Métricas")
    metrics = get_metrics()
    if metrics is None:
        st.sidebar.warning("Sin métricas. Ejecuta 'Entrenar Modelo' primero.")
        return
    st.sidebar.metric("Accuracy", f"{metrics['accuracy']:.2%}")
    st.sidebar.metric("Precision", f"{metrics['precision']:.2%}")
    st.sidebar.metric("Recall", f"{metrics['recall']:.2%}")
    st.sidebar.metric("F1-Score", f"{metrics['f1']:.2%}")
    st.sidebar.metric("AUC-ROC", f"{metrics['auc_roc']:.4f}")
    st.sidebar.divider()
    st.sidebar.caption(f"Train samples: {metrics['train_samples']:,}")
    st.sidebar.caption(f"Test samples: {metrics['test_samples']:,}")
