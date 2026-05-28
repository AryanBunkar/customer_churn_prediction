
import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Churn Prediction System",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load(
    r"C:\Users\HP\Desktop\goody\project\churn_prediction\churn_prediction.pkl"
)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Customer Churn Prediction System")

st.write(
    "Predict customer churn risk using Machine Learning"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Navigation")

option = st.sidebar.radio(
    "Choose Prediction Type",
    [
        "Single Customer Prediction",
        "Bulk CSV Prediction"
    ]
)

# ==========================================
# SINGLE CUSTOMER PREDICTION
# ==========================================

if option == "Single Customer Prediction":

    st.header("👤 Single Customer Prediction")

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        SeniorCitizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

        Partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

        Dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

        tenure = st.slider(
            "Tenure (Months)",
            0,
            72,
            12
        )

        PhoneService = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        MultipleLines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        InternetService = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        OnlineSecurity = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        OnlineBackup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

    with col2:

        DeviceProtection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

        TechSupport = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

        StreamingTV = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        StreamingMovies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

        Contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        PaperlessBilling = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

        PaymentMethod = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        MonthlyCharges = st.number_input(
            "Monthly Charges",
            min_value=0.0
        )

        TotalCharges = st.number_input(
            "Total Charges",
            min_value=0.0
        )

    # ==========================================
    # PREDICT BUTTON
    # ==========================================

    if st.button("Predict Churn"):

        customer_data = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [SeniorCitizen],
            'Partner': [Partner],
            'Dependents': [Dependents],
            'tenure': [tenure],
            'PhoneService': [PhoneService],
            'MultipleLines': [MultipleLines],
            'InternetService': [InternetService],
            'OnlineSecurity': [OnlineSecurity],
            'OnlineBackup': [OnlineBackup],
            'DeviceProtection': [DeviceProtection],
            'TechSupport': [TechSupport],
            'StreamingTV': [StreamingTV],
            'StreamingMovies': [StreamingMovies],
            'Contract': [Contract],
            'PaperlessBilling': [PaperlessBilling],
            'PaymentMethod': [PaymentMethod],
            'MonthlyCharges': [MonthlyCharges],
            'TotalCharges': [TotalCharges]
        })

        prediction = model.predict(customer_data)

        probability = model.predict_proba(customer_data)

        churn_probability = probability[0][1]

        # ==========================================
        # RESULTS
        # ==========================================

        st.subheader("Prediction Result")

        if prediction[0] == 1:
            st.error("⚠️ Customer is likely to churn")
        else:
            st.success("✅ Customer is likely to stay")

        # ==========================================
        # RISK SCORE
        # ==========================================

        st.subheader("Churn Risk Score")

        risk_percent = int(churn_probability * 100)

        st.progress(risk_percent)

        st.write(f"Churn Probability: {risk_percent}%")

        # ==========================================
        # RISK LEVEL
        # ==========================================

        if churn_probability < 0.3:
            st.success("🟢 Low Risk Customer")

        elif churn_probability < 0.6:
            st.warning("🟡 Medium Risk Customer")

        else:
            st.error("🔴 High Risk Customer")

        # ==========================================
        # BUSINESS EXPLANATION
        # ==========================================

        st.subheader("Why This Prediction?")

        reasons = []

        if Contract == "Month-to-month":
            reasons.append(
                "Customer has month-to-month contract"
            )

        if InternetService == "Fiber optic":
            reasons.append(
                "Fiber optic users show higher churn rate"
            )

        if tenure < 12:
            reasons.append(
                "Customer tenure is low"
            )

        if TechSupport == "No":
            reasons.append(
                "Customer does not use tech support"
            )

        if MonthlyCharges > 80:
            reasons.append(
                "Monthly charges are high"
            )

        if PaymentMethod == "Electronic check":
            reasons.append(
                "Electronic check users have higher churn"
            )

        if len(reasons) == 0:
            reasons.append(
                "Customer profile appears stable"
            )

        for reason in reasons:
            st.write("•", reason)

        # ==========================================
        # RETENTION STRATEGY
        # ==========================================

        st.subheader("Recommended Retention Action")

        if churn_probability > 0.7:
            st.error(
                "Offer discount and premium support immediately"
            )

        elif churn_probability > 0.5:
            st.warning(
                "Provide personalized retention offers"
            )

        else:
            st.success(
                "Customer retention risk is low"
            )

# ==========================================
# BULK CSV PREDICTION
# ==========================================

elif option == "Bulk CSV Prediction":

    st.header("📂 Bulk Customer Churn Prediction")

    st.write(
        "Upload CSV file for automatic churn prediction"
    )

    uploaded_file = st.file_uploader(
        "Drag and drop your CSV file here",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            # Read uploaded file
            bulk_data = pd.read_csv(uploaded_file)

            st.subheader("Uploaded Dataset")

            st.dataframe(bulk_data.head())

            # Make predictions
            bulk_predictions = model.predict(bulk_data)

            bulk_probabilities = (
                model.predict_proba(bulk_data)[:, 1]
            )

            # Add prediction columns
            bulk_data["Predicted_Churn"] = (
                bulk_predictions
            )

            bulk_data["Churn_Probability"] = (
                bulk_probabilities
            )

            # Convert labels
            bulk_data["Predicted_Churn"] = (
                bulk_data["Predicted_Churn"]
                .map({1: "Yes", 0: "No"})
            )

            # ==========================================
            # RISK LEVEL FUNCTION
            # ==========================================

            def risk_level(prob):

                if prob < 0.3:
                    return "Low Risk"

                elif prob < 0.6:
                    return "Medium Risk"

                else:
                    return "High Risk"

            bulk_data["Risk_Level"] = (
                bulk_data["Churn_Probability"]
                .apply(risk_level)
            )

            # ==========================================
            # DISPLAY RESULTS
            # ==========================================

            st.subheader("Prediction Results")

            st.dataframe(bulk_data)

            # ==========================================
            # ANALYTICS
            # ==========================================

            st.subheader("📈 Prediction Analytics")

            total_customers = len(bulk_data)

            churn_count = (
                bulk_data["Predicted_Churn"] == "Yes"
            ).sum()

            stay_count = (
                bulk_data["Predicted_Churn"] == "No"
            ).sum()

            high_risk_count = (
                bulk_data["Risk_Level"] == "High Risk"
            ).sum()

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Customers",
                total_customers
            )

            col2.metric(
                "Likely to Churn",
                churn_count
            )

            col3.metric(
                "Likely to Stay",
                stay_count
            )

            col4.metric(
                "High Risk Customers",
                high_risk_count
            )

            # ==========================================
            # HIGH RISK CUSTOMERS
            # ==========================================

            st.subheader("🔴 High Risk Customers")

            high_risk = bulk_data[
                bulk_data["Risk_Level"] == "High Risk"
            ]

            st.dataframe(high_risk)

            # ==========================================
            # DOWNLOAD BUTTON
            # ==========================================

            csv = bulk_data.to_csv(index=False)

            st.download_button(
                label="📥 Download Prediction Results",
                data=csv,
                file_name="churn_predictions.csv",
                mime="text/csv"
            )

        except Exception as e:

            st.error(
                f"Prediction Error: {e}"
            )
