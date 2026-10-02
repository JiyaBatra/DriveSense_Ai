import streamlit as st
import numpy as np
import joblib


# =========================================================
# MODEL PATHS
# =========================================================

MODEL_PATH = "engine_health_model.pkl"
SCALER_PATH = "engine_health_scaler.pkl"


# =========================================================
# LOAD MODEL AND SCALER
# =========================================================

@st.cache_resource
def load_engine_model():

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    return model, scaler


# =========================================================
# VEHICLE HEALTH PAGE
# =========================================================

def show_vehicle_health():

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="main-title">
            Vehicle Health
        </div>

        <div class="page-subtitle">
            AI-powered engine condition monitoring
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # LOAD MODEL
    # -----------------------------------------------------

    try:

        model, scaler = load_engine_model()

    except Exception as e:

        st.error(
            "Vehicle health model could not be loaded."
        )

        st.code(str(e))

        return

    # -----------------------------------------------------
    # ENGINE SENSOR INPUT
    # -----------------------------------------------------

    st.markdown("### Engine Sensor Data")

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

    with col1:

        engine_rpm = st.number_input(
            "Engine RPM",
            min_value=0.0,
            value=2830.0,
            step=10.0
        )

        lub_oil_pressure = st.number_input(
            "Lub Oil Pressure",
            min_value=0.0,
            value=3.0,
            step=0.1
        )

        fuel_pressure = st.number_input(
            "Fuel Pressure",
            min_value=0.0,
            value=10.0,
            step=0.1
        )

    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

    with col2:

        coolant_pressure = st.number_input(
            "Coolant Pressure",
            min_value=0.0,
            value=2.6,
            step=0.1
        )

        lub_oil_temp = st.number_input(
            "Lub Oil Temperature",
            min_value=0.0,
            value=75.0,
            step=0.5
        )

        coolant_temp = st.number_input(
            "Coolant Temperature",
            min_value=0.0,
            value=80.0,
            step=0.5
        )

    st.markdown("")

    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    if st.button(
        "Analyze Vehicle Health",
        use_container_width=True
    ):

        # -------------------------------------------------
        # CREATE INPUT
        # -------------------------------------------------

        input_data = np.array(
            [[
                engine_rpm,
                lub_oil_pressure,
                fuel_pressure,
                coolant_pressure,
                lub_oil_temp,
                coolant_temp
            ]]
        )

        # -------------------------------------------------
        # SCALE INPUT
        # -------------------------------------------------

        input_scaled = scaler.transform(
            input_data
        )

        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = model.predict(
            input_scaled
        )[0]

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.markdown("---")

        st.markdown(
            "### Vehicle Health Result"
        )

        if prediction == 1:

            st.success(
                "Engine Condition: Healthy"
            )

        else:

            st.error(
                "Engine Condition: Needs Attention"
            )

        # -------------------------------------------------
        # SENSOR SUMMARY
        # -------------------------------------------------

        st.markdown(
            "### Sensor Summary"
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:

            st.metric(
                "Engine RPM",
                f"{engine_rpm:.0f}"
            )

        with result_col2:

            st.metric(
                "Lub Oil Pressure",
                f"{lub_oil_pressure:.2f}"
            )

        with result_col3:

            st.metric(
                "Fuel Pressure",
                f"{fuel_pressure:.2f}"
            )

        result_col4, result_col5, result_col6 = st.columns(3)

        with result_col4:

            st.metric(
                "Coolant Pressure",
                f"{coolant_pressure:.2f}"
            )

        with result_col5:

            st.metric(
                "Lub Oil Temp",
                f"{lub_oil_temp:.1f}"
            )

        with result_col6:

            st.metric(
                "Coolant Temp",
                f"{coolant_temp:.1f}"
            )