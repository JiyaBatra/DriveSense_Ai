import streamlit as st

# =========================================================
# IMPORT FEATURE MODULES
# =========================================================

from drowsiness import show_drowsiness
from vehicle_health import show_vehicle_health
from lane_detection import show_lane_detection


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DriveSense AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------
       MAIN APP
    ------------------------------------------------- */

    .stApp {
        background-color: #071A2B;
        color: #FFFFFF;
    }

    /* -------------------------------------------------
       SIDEBAR
    ------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #061523;
        border-right: 1px solid #173A55;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    /* -------------------------------------------------
       TITLES
    ------------------------------------------------- */

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 5px;
    }

    .page-subtitle {
        font-size: 16px;
        color: #9FB6C8;
        margin-bottom: 25px;
    }

    /* -------------------------------------------------
       DASHBOARD CARDS
    ------------------------------------------------- */

    .feature-card {
        background-color: #0D263B;
        border: 1px solid #214B67;
        border-radius: 14px;
        padding: 25px;
        min-height: 170px;
        margin-bottom: 20px;
    }

    .feature-title {
        font-size: 21px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    .feature-description {
        font-size: 14px;
        color: #A9BECE;
        line-height: 1.6;
    }

    /* -------------------------------------------------
       BUTTONS
    ------------------------------------------------- */

    .stButton > button {
        background-color: #123E5A;
        color: white;
        border: 1px solid #2B6588;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 20px;
    }

    .stButton > button:hover {
        background-color: #185171;
        border-color: #3B789D;
    }

    /* -------------------------------------------------
       METRICS
    ------------------------------------------------- */

    div[data-testid="stMetric"] {
        background-color: #0D263B;
        border: 1px solid #214B67;
        padding: 15px;
        border-radius: 10px;
    }

    /* -------------------------------------------------
       DIVIDER
    ------------------------------------------------- */

    hr {
        border-color: #214B67;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:700;
            margin-bottom:5px;
        ">
            DriveSense AI
        </div>

        <div style="
            font-size:13px;
            color:#9FB6C8;
            margin-bottom:25px;
        ">
            Smart Mobility & Vehicle Safety
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Navigation
    # -----------------------------------------------------

    if st.button(
        "Dashboard",
        use_container_width=True
    ):
        st.session_state.page = "Dashboard"

    if st.button(
        "Drowsiness Detection",
        use_container_width=True
    ):
        st.session_state.page = "Drowsiness Detection"

    if st.button(
        "Vehicle Health",
        use_container_width=True
    ):
        st.session_state.page = "Vehicle Health"

    if st.button(
        "Lane Detection",
        use_container_width=True
    ):
        st.session_state.page = "Lane Detection"

    if st.button(
        "Accident Risk",
        use_container_width=True
    ):
        st.session_state.page = "Accident Risk"

    st.markdown("---")

    if st.button(
        "My Profile",
        use_container_width=True
    ):
        st.session_state.page = "My Profile"

    if st.button(
        "Notifications",
        use_container_width=True
    ):
        st.session_state.page = "Notifications"


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        """
        <div class="main-title">
            DriveSense AI
        </div>

        <div class="page-subtitle">
            AI-powered vehicle safety and smart mobility platform
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Safety & Monitoring")

    # -----------------------------------------------------
    # ROW 1
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-title">
                    Drowsiness Detection
                </div>

                <div class="feature-description">
                    Monitor driver alertness using computer
                    vision and CNN-based facial analysis.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Drowsiness Detection",
            key="dashboard_drowsiness",
            use_container_width=True
        ):
            st.session_state.page = "Drowsiness Detection"
            st.rerun()

    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-title">
                    Vehicle Health
                </div>

                <div class="feature-description">
                    Analyze engine sensor parameters and
                    predict the current engine condition.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Vehicle Health",
            key="dashboard_vehicle",
            use_container_width=True
        ):
            st.session_state.page = "Vehicle Health"
            st.rerun()

    # -----------------------------------------------------
    # ROW 2
    # -----------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-title">
                    Lane Detection
                </div>

                <div class="feature-description">
                    Detect road lanes in real time using
                    OpenCV, edge detection and Hough transforms.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Lane Detection",
            key="dashboard_lane",
            use_container_width=True
        ):
            st.session_state.page = "Lane Detection"
            st.rerun()

    with col4:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-title">
                    Accident Risk
                </div>

                <div class="feature-description">
                    Intelligent accident risk monitoring and
                    safety alerts.
                    <br><br>
                    <b>Coming Soon</b>
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# DROWSINESS PAGE
# =========================================================

elif st.session_state.page == "Drowsiness Detection":

    show_drowsiness()


# =========================================================
# VEHICLE HEALTH PAGE
# =========================================================

elif st.session_state.page == "Vehicle Health":

    show_vehicle_health()


# =========================================================
# LANE DETECTION PAGE
# =========================================================

elif st.session_state.page == "Lane Detection":

    show_lane_detection()


# =========================================================
# ACCIDENT RISK
# =========================================================

elif st.session_state.page == "Accident Risk":

    st.markdown(
        """
        <div class="main-title">
            Accident Risk
        </div>

        <div class="page-subtitle">
            Intelligent accident risk monitoring
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Accident Risk module is currently under development."
    )


# =========================================================
# MY PROFILE
# =========================================================

elif st.session_state.page == "My Profile":

    st.markdown(
        """
        <div class="main-title">
            My Profile
        </div>

        <div class="page-subtitle">
            DriveSense AI user profile
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### Jiya Batra

            **Role:** Developer / AI Project Team

            **Project:** DriveSense AI

            **Focus:** AI, Computer Vision & Smart Mobility
            """
        )

    with col2:

        st.metric(
            "Active Modules",
            "3"
        )

        st.metric(
            "Platform",
            "DriveSense AI"
        )


# =========================================================
# NOTIFICATIONS
# =========================================================

elif st.session_state.page == "Notifications":

    st.markdown(
        """
        <div class="main-title">
            Notifications
        </div>

        <div class="page-subtitle">
            Safety and system notifications
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "No new notifications."
    )