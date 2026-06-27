import streamlit as st
from app.api_client import trigger_train, get_train_status
from app.components.metrics_panel import render_metrics_panel
from app.components.prediction_form import render_prediction_form

st.set_page_config(
    page_title="NEXUS-DS",
    page_icon="🔮",
    layout="wide",
)

# Panel lateral: métricas del modelo
render_metrics_panel()

# Cuerpo principal
st.title("NEXUS-DS")
st.caption("Next-generation EXecution & Unified System for Data Science")
st.divider()

# Sección de entrenamiento
with st.expander("Gestión del Modelo", expanded=False):
    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        if st.button("Entrenar Modelo", use_container_width=True):
            resp = trigger_train()
            st.info(resp.get("message", str(resp)))
    with col_status:
        if st.button("Ver Estado del Entrenamiento", use_container_width=True):
            status = get_train_status()
            st.json(status)

st.divider()

# Formulario de predicción
render_prediction_form()
