import base64
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import streamlit as st

# =========================================================
# IMPORT FEATURE MODULES
# =========================================================

from drowsiness import show_drowsiness
from vehicle_health import show_vehicle_health
from lane_detection import show_lane_detection
from accident_risk import show_accident_risk


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
# HTML HELPERS
# Markdown treats lines indented by 4+ spaces as a code block,
# so HTML is flattened into a single line before rendering.
# =========================================================

def html_block(html: str) -> str:
    return "".join(line.strip() for line in html.splitlines())


def render_html(html: str):
    st.markdown(html_block(html), unsafe_allow_html=True)


def page_header(title: str, subtitle: str):
    render_html(
        f"""
        <div class="main-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        """
    )


def feature_card(title: str, description: str, status: str, live: bool = True):
    pill_class = "pill-live" if live else "pill-soon"
    render_html(
        f"""
        <div class="feature-card">
            <div class="feature-title">{title}</div>
            <div class="feature-description">{description}</div>
            <div class="status-pill {pill_class}">{status}</div>
        </div>
        """
    )


# =========================================================
# CAR BACKGROUND
# Uses assets/Car.jpeg if present (also Car.jpg / Car.png /
# car_bg.jpg), otherwise a built-in black SUV with glowing lights.
# =========================================================

CAR_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520">
  <defs>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#262c36"/>
      <stop offset="1" stop-color="#05070A"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#303948"/>
      <stop offset="1" stop-color="#090c11"/>
    </linearGradient>
    <radialGradient id="beam">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".85"/>
      <stop offset=".35" stop-color="#bfe9ff" stop-opacity=".28"/>
      <stop offset="1" stop-color="#7fd6ff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="floor">
      <stop offset="0" stop-color="#7fd6ff" stop-opacity=".38"/>
      <stop offset="1" stop-color="#7fd6ff" stop-opacity="0"/>
    </radialGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
  </defs>

  <ellipse cx="400" cy="478" rx="370" ry="36" fill="url(#floor)"/>

  <circle cx="234" cy="351" r="125" fill="url(#beam)"/>
  <circle cx="566" cy="351" r="125" fill="url(#beam)"/>

  <rect x="150" y="392" width="84" height="88" rx="16" fill="#050607"/>
  <rect x="566" y="392" width="84" height="88" rx="16" fill="#050607"/>

  <rect x="148" y="268" width="48" height="24" rx="9" fill="#0b0d11"/>
  <rect x="604" y="268" width="48" height="24" rx="9" fill="#0b0d11"/>

  <path d="M236 186 Q400 164 564 186 L612 304 L188 304 Z" fill="url(#glass)"/>
  <path d="M236 186 Q400 164 564 186" stroke="#ffffff" stroke-opacity=".2"
        stroke-width="3" fill="none"/>
  <path d="M246 176 Q400 154 554 176" stroke="#3a414d" stroke-width="5"
        fill="none" stroke-linecap="round"/>
  <path d="M300 200 L350 300 M330 196 L372 300" stroke="#ffffff"
        stroke-opacity=".05" stroke-width="14"/>

  <path d="M150 318 Q152 296 188 300 L612 300 Q648 296 650 318
           L660 408 Q660 440 630 446 L170 446 Q140 440 140 408 Z"
        fill="url(#body)"/>
  <path d="M188 304 L612 304" stroke="#ffffff" stroke-opacity=".14" stroke-width="2"/>
  <path d="M168 440 L632 440" stroke="#ffffff" stroke-opacity=".07" stroke-width="2"/>

  <path d="M290 372 L510 372 L492 418 L308 418 Z" fill="#030405"/>
  <path d="M300 384 H500 M304 396 H496 M308 408 H492" stroke="#1b2027" stroke-width="3"/>
  <rect x="330" y="428" width="140" height="9" rx="4.5" fill="#1b2027"/>

  <rect x="196" y="318" width="408" height="7" rx="3.5" fill="#7fd6ff"
        filter="url(#blur)" opacity=".95"/>
  <rect x="196" y="318" width="408" height="7" rx="3.5" fill="#eaf8ff"/>

  <rect x="176" y="336" width="116" height="30" rx="14" fill="#090c10" stroke="#2a313b"/>
  <rect x="508" y="336" width="116" height="30" rx="14" fill="#090c10" stroke="#2a313b"/>
  <circle cx="214" cy="351" r="17" fill="#bfe9ff" filter="url(#blur)" opacity=".9"/>
  <circle cx="586" cy="351" r="17" fill="#bfe9ff" filter="url(#blur)" opacity=".9"/>
  <circle cx="214" cy="351" r="8" fill="#ffffff"/>
  <circle cx="586" cy="351" r="8" fill="#ffffff"/>
  <rect x="236" y="346" width="46" height="5" rx="2.5" fill="#eaf8ff"/>
  <rect x="518" y="346" width="46" height="5" rx="2.5" fill="#eaf8ff"/>

  <ellipse cx="250" cy="404" rx="22" ry="10" fill="#7fd6ff" filter="url(#blur)" opacity=".7"/>
  <ellipse cx="550" cy="404" rx="22" ry="10" fill="#7fd6ff" filter="url(#blur)" opacity=".7"/>
  <ellipse cx="250" cy="404" rx="14" ry="5.5" fill="#eaf8ff"/>
  <ellipse cx="550" cy="404" rx="14" ry="5.5" fill="#eaf8ff"/>
</svg>
"""


@st.cache_data
def get_car_background_css():
    """Returns the CSS 'background' value for the car layer."""
    assets = Path(__file__).resolve().parent / "assets"

    candidates = [
        ("Car.jpeg", "image/jpeg"),
        ("Car.jpg", "image/jpeg"),
        ("Car.png", "image/png"),
        ("car_bg.jpg", "image/jpeg"),
    ]

    for name, mime in candidates:
        photo = assets / name
        if photo.exists():
            b64 = base64.b64encode(photo.read_bytes()).decode()
            return (
                "linear-gradient(90deg, rgba(0,0,0,0.88) 0%, "
                "rgba(0,0,0,0.60) 45%, rgba(0,0,0,0.25) 100%), "
                f"url('data:{mime};base64,{b64}') center right / cover no-repeat, "
                "#000"
            )

    svg_uri = "data:image/svg+xml;utf8," + quote(CAR_SVG)
    return (
        "linear-gradient(90deg, rgba(0,0,0,0.90) 0%, "
        "rgba(0,0,0,0.55) 42%, rgba(0,0,0,0.05) 100%), "
        f"url(\"{svg_uri}\") no-repeat right 3% bottom 4% / min(66vw, 1050px) auto, "
        "radial-gradient(ellipse at 75% 95%, rgba(127,214,255,0.18) 0%, transparent 55%), "
        "linear-gradient(180deg, #0d1016 0%, #07090c 55%, #000000 100%)"
    )


# =========================================================
# CUSTOM CSS  (Black car theme: white text + ice-blue light accent)
# =========================================================

CSS = """
<style>

:root {
    --accent: #7FD6FF;
    --accent-soft: #BFE9FF;
    --accent-glow: rgba(127, 214, 255, 0.45);
    --tail: #FF4D4D;
    --ok: #4ADE80;
    --white: #FFFFFF;
    --card: rgba(12, 15, 20, 0.72);
    --border: rgba(255, 255, 255, 0.12);
}

/* ---------------- MAIN APP ---------------- */

.stApp {
    background: #000;
    color: var(--white);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background: __CAR_BG__;
}

.block-container {
    position: relative;
    z-index: 1;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* ---------------- TEXT ---------------- */

.stApp p,
.stApp li,
.stApp label,
.stApp span,
.stApp div[data-testid="stMarkdownContainer"] {
    color: var(--white);
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: var(--accent) !important;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10, 12, 16, 0.96) 0%, rgba(2, 3, 5, 0.98) 100%);
    border-right: 1px solid rgba(127, 214, 255, 0.28);
    box-shadow: 4px 0 22px rgba(127, 214, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: var(--white);
}

.sidebar-brand {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sidebar-tagline {
    font-size: 13px;
    color: var(--accent-soft) !important;
    margin-bottom: 25px;
}

/* ---------------- TITLES ---------------- */

.main-title {
    font-size: 38px;
    font-weight: 700;
    color: var(--white) !important;
    margin-bottom: 5px;
    text-shadow: 0 0 20px var(--accent-glow);
}

.page-subtitle {
    font-size: 16px;
    color: var(--accent-soft) !important;
    margin-bottom: 25px;
}

/* ---------------- DASHBOARD CARDS ---------------- */

.feature-card {
    position: relative;
    overflow: hidden;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 25px;
    min-height: 170px;
    margin-bottom: 14px;
    backdrop-filter: blur(8px);
    transition: all 0.25s ease;
}

.feature-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 8%;
    right: 8%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.55;
    transition: opacity 0.25s ease;
}

.feature-card:hover {
    border-color: var(--accent);
    box-shadow: 0 0 26px var(--accent-glow);
    transform: translateY(-2px);
}

.feature-card:hover::before {
    opacity: 1;
}

.feature-title {
    font-size: 21px;
    font-weight: 600;
    color: var(--white) !important;
    margin-bottom: 10px;
}

.feature-description {
    font-size: 14px;
    color: #E1E6EE !important;
    line-height: 1.6;
    margin-bottom: 14px;
}

.status-pill {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 12px;
    border-radius: 999px;
    letter-spacing: 0.3px;
}

.pill-live {
    color: var(--ok) !important;
    background: rgba(74, 222, 128, 0.12);
    border: 1px solid rgba(74, 222, 128, 0.45);
}

.pill-soon {
    color: var(--tail) !important;
    background: rgba(255, 77, 77, 0.12);
    border: 1px solid rgba(255, 77, 77, 0.45);
}

/* ---------------- BUTTONS ---------------- */

.stButton > button {
    background: linear-gradient(180deg, #1c222b 0%, #0b0e13 100%);
    color: var(--white);
    border: 1px solid rgba(127, 214, 255, 0.35);
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #232b36 0%, #0f141b 100%);
    border-color: var(--accent);
    box-shadow: 0 0 16px var(--accent-glow);
    color: var(--white);
}

/* ---------------- METRICS ---------------- */

div[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    padding: 15px;
    border-radius: 10px;
    backdrop-filter: blur(8px);
}

div[data-testid="stMetricLabel"] * {
    color: var(--accent-soft) !important;
}

div[data-testid="stMetricValue"] * {
    color: var(--white) !important;
}

/* ---------------- CHARTS / TABLES ---------------- */

div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stDataFrame"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px;
    backdrop-filter: blur(8px);
}

.chart-note {
    font-size: 12px;
    color: var(--accent-soft) !important;
    margin-top: 6px;
}

/* ---------------- DIVIDER ---------------- */

hr {
    border-color: rgba(255, 255, 255, 0.14);
}

/* ---------------- MOBILE ---------------- */

@media (max-width: 800px) {
    .stApp::before {
        opacity: 0.55;
    }
}

</style>
"""

st.markdown(
    CSS.replace("__CAR_BG__", get_car_background_css()),
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

NAV_ITEMS = [
    "Dashboard",
    "Drowsiness Detection",
    "Vehicle Health",
    "Lane Detection",
    "Accident Risk",
]

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">DriveSense AI</div>
        <div class="sidebar-tagline">Smart Mobility & Vehicle Safety</div>
        """
    )

    for item in NAV_ITEMS:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()

    st.markdown("---")

    for item in ["My Profile", "Notifications"]:
        if st.button(item, key=f"nav_{item}", use_container_width=True):
            st.session_state.page = item
            st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":

    page_header(
        "DriveSense AI",
        "AI-powered vehicle safety and smart mobility platform",
    )

    # ---------------- Summary metrics ----------------

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Modules Live", "4 / 4")
    m2.metric("Alert Delay", "2 sec")
    m3.metric("Input", "Live Camera")
    m4.metric("Risk Engine", "Fusion")

    st.markdown("### Safety & Monitoring")

    # ---------------- Row 1 ----------------

    col1, col2 = st.columns(2)

    with col1:
        feature_card(
            "Drowsiness Detection",
            "Monitor driver alertness using computer vision and "
            "CNN-based facial analysis with an audible alarm.",
            "● LIVE",
        )
        if st.button(
            "Open Drowsiness Detection",
            key="dashboard_drowsiness",
            use_container_width=True,
        ):
            st.session_state.page = "Drowsiness Detection"
            st.rerun()

    with col2:
        feature_card(
            "Vehicle Health",
            "Analyze engine sensor parameters and predict the "
            "current engine condition.",
            "● LIVE",
        )
        if st.button(
            "Open Vehicle Health",
            key="dashboard_vehicle",
            use_container_width=True,
        ):
            st.session_state.page = "Vehicle Health"
            st.rerun()

    # ---------------- Row 2 ----------------

    col3, col4 = st.columns(2)

    with col3:
        feature_card(
            "Lane Detection",
            "Detect road lanes in real time using OpenCV, edge "
            "detection and Hough transforms.",
            "● LIVE",
        )
        if st.button(
            "Open Lane Detection",
            key="dashboard_lane",
            use_container_width=True,
        ):
            st.session_state.page = "Lane Detection"
            st.rerun()

    with col4:
        feature_card(
            "Accident Risk",
            "Combines drowsiness, lane keeping and vehicle health "
            "into one live accident risk score.",
            "● LIVE",
        )
        if st.button(
            "Open Accident Risk",
            key="dashboard_accident",
            use_container_width=True,
        ):
            st.session_state.page = "Accident Risk"
            st.rerun()

    # ---------------- Overview table + chart ----------------

    st.markdown("### System Overview")

    overview = pd.DataFrame(
        {
            "Module": [
                "Drowsiness Detection",
                "Vehicle Health",
                "Lane Detection",
                "Accident Risk",
            ],
            "Technique": [
                "CNN + Haar face detector",
                "Random Forest on engine sensors",
                "Canny edges + Hough lines",
                "Weighted risk fusion",
            ],
            "Input": [
                "Live camera",
                "Sensor values",
                "Camera / image",
                "Module signals",
            ],
            "Status": ["Live", "Live", "Live", "Live"],
        }
    )
    st.dataframe(overview, use_container_width=True, hide_index=True)

    st.markdown("### Driver Alertness Trend")

    # SAMPLE DATA for the demo. Replace with real logged values later.
    trend = pd.DataFrame(
        {
            "Alertness %": [92, 88, 85, 90, 78, 84, 91],
            "Drowsy events": [1, 2, 4, 2, 6, 3, 1],
        },
        index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.line_chart(trend[["Alertness %"]], color="#7FD6FF")

    with chart_col2:
        st.bar_chart(trend[["Drowsy events"]], color="#FF4D4D")

    render_html(
        '<div class="chart-note">Sample data for demonstration. '
        "Connect real detection logs to show live values.</div>"
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
# ACCIDENT RISK PAGE
# =========================================================

elif st.session_state.page == "Accident Risk":

    show_accident_risk()


# =========================================================
# MY PROFILE
# =========================================================

elif st.session_state.page == "My Profile":

    page_header(
        "My Profile",
        "DriveSense AI user profile",
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
        st.metric("Active Modules", "4")
        st.metric("Platform", "DriveSense AI")


# =========================================================
# NOTIFICATIONS
# =========================================================

elif st.session_state.page == "Notifications":

    page_header(
        "Notifications",
        "Safety and system notifications",
    )

    st.info(
        "No new notifications."
    )