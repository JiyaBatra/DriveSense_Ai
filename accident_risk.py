import pandas as pd
import streamlit as st

from signals import read
from drowsiness import load_alarm_audio

WEIGHTS = {"drowsiness": 0.45, "lane": 0.30, "vehicle": 0.25}
NAMES = {
    "drowsiness": "Driver Drowsiness",
    "lane": "Lane Keeping",
    "vehicle": "Vehicle Health",
}
LIVE_MAX_AGE = 5.0         # seconds a camera signal stays valid
VEHICLE_MAX_AGE = 900.0    # vehicle prediction stays valid longer

ADVICE = {
    "LOW": "Conditions look safe. Keep monitoring.",
    "MODERATE": "Stay alert. One or more risk factors are rising.",
    "HIGH": "High accident risk. Slow down and take a break at the next safe spot.",
    "CRITICAL": "Critical risk. Pull over safely as soon as possible.",
}


# =========================================================
# HELPERS
# =========================================================

def _html(html: str) -> str:
    return "".join(line.strip() for line in html.splitlines())


def _render(html: str):
    st.markdown(_html(html), unsafe_allow_html=True)


def _clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, float(x)))


# =========================================================
# RISK RULES (each returns 0-100)
# =========================================================

def drowsiness_risk(awake_pct, alarm=False):
    # awake 90%+ -> 0 risk, awake 40% or less -> 100 risk
    risk = _clamp((90 - awake_pct) * 2)
    if alarm:
        risk = max(risk, 90)
    return risk


def lane_risk(status, offset):
    # offset = vehicle position vs lane centre, as a fraction of lane width
    if offset is not None:
        # 0.10 off-centre -> 0 risk, 0.40 off-centre -> 100 risk
        return _clamp((abs(offset) - 0.10) / 0.30 * 100)
    if status == "ONE LANE":
        return 35.0
    return 30.0   # no lane found: low confidence, mild risk


def vehicle_risk(item):
    if item is None:
        return None
    if "risk" in item:
        return _clamp(item["risk"])

    label = str(item.get("label", "")).strip().lower()
    good = ("good", "normal", "healthy", "ok", "safe")
    warn = ("warning", "moderate", "medium", "average", "caution", "minor")
    bad = ("critical", "bad", "fault", "fail", "danger", "poor", "high", "severe")

    if label in ("0", "0.0") or any(w in label for w in good):
        return 0.0
    if any(w in label for w in warn):
        return 50.0
    if label in ("1", "1.0") or any(w in label for w in bad):
        return 100.0
    return 50.0


def combine(parts):
    """parts: {name: risk or None}. Returns (score, contributions, bonus)."""
    avail = {k: v for k, v in parts.items() if v is not None}
    if not avail:
        return None, {}, 0

    wsum = sum(WEIGHTS[k] for k in avail)
    contrib = {k: WEIGHTS[k] * v / wsum for k, v in avail.items()}
    base = sum(contrib.values())

    d, l, v = parts.get("drowsiness"), parts.get("lane"), parts.get("vehicle")
    bonus = 0
    if d is not None and l is not None and d >= 60 and l >= 50:
        bonus += 15      # sleepy AND drifting
    if d is not None and v is not None and d >= 60 and v >= 50:
        bonus += 10      # sleepy AND vehicle problem
    if l is not None and v is not None and l >= 50 and v >= 50:
        bonus += 5

    score = min(100.0, base + bonus)
    # a single very dangerous factor must not be diluted by the others
    score = max(score, 0.7 * max(avail.values()))
    return score, contrib, bonus


def risk_level(score):
    if score < 30:
        return "LOW", "#4ADE80"
    if score < 60:
        return "MODERATE", "#FACC15"
    if score < 80:
        return "HIGH", "#FB923C"
    return "CRITICAL", "#FF4D4D"


# =========================================================
# INPUT COLLECTION
# =========================================================

def collect_live():
    parts, info = {}, {}

    d = read("drowsiness", LIVE_MAX_AGE)
    if d and d.get("awake_pct") is not None:
        parts["drowsiness"] = drowsiness_risk(d["awake_pct"], d.get("alarm", False))
        info["drowsiness"] = f"Awake {d['awake_pct']:.0f}%" + (" | alarm" if d.get("alarm") else "")
    else:
        parts["drowsiness"], info["drowsiness"] = None, "No live data"

    l = read("lane", LIVE_MAX_AGE)
    if l:
        parts["lane"] = lane_risk(l.get("status"), l.get("offset"))
        off = l.get("offset")
        info["lane"] = f"{l.get('status')}" + (f" | offset {off:+.2f}" if off is not None else "")
    else:
        parts["lane"], info["lane"] = None, "No live data"

    v = read("vehicle", VEHICLE_MAX_AGE)
    parts["vehicle"] = vehicle_risk(v)
    info["vehicle"] = f"Result: {v.get('label', v.get('risk'))}" if v else "No prediction yet"

    return parts, info


# =========================================================
# RESULT UI
# =========================================================

def render_result(parts, info, mute, track_history=False):
    score, contrib, bonus = combine(parts)

    if score is None:
        st.warning("No signals available yet. Start a module or use Manual simulation.")
        return

    name, color = risk_level(score)
    top = max(contrib, key=contrib.get)

    _render(
        f"""
        <div class="feature-card" style="border-color:{color};box-shadow:0 0 26px {color}55;">
        <div style="font-size:13px;letter-spacing:1px;color:#BFE9FF;">ACCIDENT RISK SCORE</div>
        <div style="font-size:54px;font-weight:800;color:{color};line-height:1.1;">{score:.0f}<span style="font-size:22px;color:#FFFFFF;"> / 100</span></div>
        <div style="font-size:18px;font-weight:700;color:{color};margin-bottom:12px;">{name}</div>
        <div style="height:12px;border-radius:6px;background:rgba(255,255,255,0.12);overflow:hidden;"><div style="width:{score:.0f}%;height:100%;background:{color};"></div></div>
        <div style="margin-top:12px;font-size:14px;color:#E1E6EE;">{ADVICE[name]}</div>
        <div style="margin-top:6px;font-size:13px;color:#BFE9FF;">Biggest factor: {NAMES[top]}</div>
        </div>
        """
    )

    if bonus > 0:
        st.warning(f"Combined-risk boost +{bonus}: multiple factors are bad at the same time.")

    cols = st.columns(3)
    for col, key in zip(cols, ["drowsiness", "lane", "vehicle"]):
        value = "-" if parts[key] is None else f"{parts[key]:.0f}"
        col.metric(NAMES[key], value)
        col.caption(info[key])

    st.markdown("### Risk Contribution")
    st.bar_chart(
        pd.Series({NAMES[k]: v for k, v in contrib.items()}, name="Risk points"),
        color="#7FD6FF",
    )

    if track_history:
        hist = st.session_state.setdefault("risk_history", [])
        hist.append(score)
        del hist[:-120]
        st.markdown("### Risk Over Time")
        st.line_chart(pd.DataFrame({"Risk score": hist}), color="#FF4D4D")

    if name in ("HIGH", "CRITICAL") and not mute:
        audio_bytes, audio_mime = load_alarm_audio()
        st.audio(audio_bytes, format=audio_mime, autoplay=True, loop=True)


def _live_panel(mute):
    parts, info = collect_live()
    render_result(parts, info, mute, track_history=True)


if hasattr(st, "fragment"):
    live_panel = st.fragment(run_every=1)(_live_panel)   # auto-refresh every second
else:
    live_panel = _live_panel


# =========================================================
# PAGE
# =========================================================

def show_accident_risk():
    _render(
        """
        <div class="main-title">Accident Risk Prediction</div>
        <div class="page-subtitle">Driver drowsiness, lane keeping and vehicle health combined into one risk score</div>
        """
    )

    mode = st.radio(
        "Data source",
        ["Manual simulation", "Live from modules"],
        horizontal=True,
    )
    mute = st.checkbox("Mute alarm", value=False)

    # ---------------- Manual simulation ----------------
    if mode == "Manual simulation":
        st.markdown("### Simulate Conditions")
        c1, c2, c3 = st.columns(3)

        with c1:
            awake = st.slider("Driver awake %", 0, 100, 95)
        with c2:
            offset = st.slider("Lane offset (left -0.5 ... right +0.5)", -0.5, 0.5, 0.0, 0.05)
            lost = st.checkbox("Lane markings lost")
        with c3:
            vehicle = st.select_slider(
                "Vehicle condition", ["Good", "Warning", "Critical"]
            )

        parts = {
            "drowsiness": drowsiness_risk(awake, alarm=awake < 60),
            "lane": lane_risk("NO LANE", None) if lost else lane_risk("BOTH LANES", offset),
            "vehicle": {"Good": 0.0, "Warning": 50.0, "Critical": 100.0}[vehicle],
        }
        info = {
            "drowsiness": f"Awake {awake}%",
            "lane": "Lane lost" if lost else f"Offset {offset:+.2f}",
            "vehicle": vehicle,
        }
        render_result(parts, info, mute)
        return

    # ---------------- Live mode ----------------
    with st.expander("How live mode works"):
        st.markdown(
            "- Open **Drowsiness Detection** and **Lane Detection** (each uses its own camera) "
            "and run **Vehicle Health** once.\n"
            "- Each module sends its latest result here. Camera signals expire after "
            "5 seconds, so they must keep running.\n"
            "- A browser tab runs one page at a time, so use **separate tabs or devices** "
            "(for example laptop webcam for the driver, phone for the road) and keep this page "
            "open in another tab."
        )

    live_panel(mute)