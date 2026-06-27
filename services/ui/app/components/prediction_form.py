import streamlit as st
from app.api_client import predict


def render_prediction_form():
    st.subheader("Datos del Cliente")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Género", ["Male", "Female"])
        senior = st.selectbox("Senior Citizen", [0, 1])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        tenure = st.slider("Tenure (meses)", 0, 72, 12)
        monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 65.0, step=0.5)
        total_charges = st.number_input("Total Charges ($)", 0.0, 10000.0, 780.0, step=1.0)

    with col2:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox(
            "Multiple Lines", ["Yes", "No", "No phone service"]
        )
        internet_service = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        online_security = st.selectbox(
            "Online Security", ["Yes", "No", "No internet service"]
        )
        online_backup = st.selectbox(
            "Online Backup", ["Yes", "No", "No internet service"]
        )
        device_protection = st.selectbox(
            "Device Protection", ["Yes", "No", "No internet service"]
        )

    with col3:
        tech_support = st.selectbox(
            "Tech Support", ["Yes", "No", "No internet service"]
        )
        streaming_tv = st.selectbox(
            "Streaming TV", ["Yes", "No", "No internet service"]
        )
        streaming_movies = st.selectbox(
            "Streaming Movies", ["Yes", "No", "No internet service"]
        )
        contract = st.selectbox(
            "Contract", ["Month-to-month", "One year", "Two year"]
        )
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )

    st.divider()

    if st.button("Predecir Churn", type="primary", use_container_width=True):
        payload = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }
        try:
            result = predict(payload)
            _render_result(result)
        except Exception as e:
            st.error(f"Error al predecir: {e}")


def _render_result(result: dict):
    churn = result["churn"]
    prob = result["probability"]
    prob_pct = prob * 100

    st.divider()
    if churn == "Yes":
        st.error(f"Churn Predicho: **SÍ** — Probabilidad: **{prob_pct:.1f}%**")
    else:
        st.success(f"Churn Predicho: **NO** — Probabilidad de churn: **{prob_pct:.1f}%**")

    st.progress(prob)
    st.caption(f"Probabilidad raw: {prob:.4f}")
