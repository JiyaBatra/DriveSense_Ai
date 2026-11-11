
import io
import os
import time
import wave
from pathlib import Path

# Memory optimization: set before importing TensorFlow
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import cv2
cv2.setNumThreads(1)

import av
import numpy as np
import streamlit as st
import tensorflow as tf

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration,
)

from signals import publish


# =========================================================
# CONFIGURATION
# =========================================================

MODEL_PATH = Path(__file__).resolve().parent / "drowsiness_model.keras"

ALARM_CANDIDATES = [
    Path(__file__).resolve().parent / "assets" / "AlertAlarm.aac",
    Path("assets") / "AlertAlarm.aac",
]

ALARM_MIME = "audio/aac"


# =========================================================
# WEBRTC CONFIGURATION
# =========================================================

def get_rtc_config():
    """Configure STUN and optional TURN servers."""

    servers = [
        {"urls": ["stun:stun.l.google.com:19302"]}
    ]

    try:
        turn = st.secrets["turn"]

        servers.append({
            "urls": [turn["url"]],
            "username": turn["username"],
            "credential": turn["credential"],
        })

    except Exception:
        pass

    return RTCConfiguration({"iceServers": servers})


# =========================================================
# LOADERS
# =========================================================

@st.cache_resource
def load_drowsiness_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    return tf.keras.models.load_model(MODEL_PATH)


@st.cache_resource
def load_face_detector():

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    if detector.empty():
        raise RuntimeError("Unable to load Haar face detector.")

    return detector


@st.cache_data
def make_fallback_beep(
    duration=1.0,
    freq=880,
    rate=44100
):
    """Generate a fallback alarm."""

    t = np.linspace(
        0,
        duration,
        int(rate * duration),
        False
    )

    beep_mask = np.sin(2 * np.pi * 4 * t) > 0

    tone = (
        np.sin(2 * np.pi * freq * t)
        * beep_mask
        * 0.8
    )

    data = (tone * 32767).astype(np.int16)

    buf = io.BytesIO()

    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(data.tobytes())

    return buf.getvalue()


@st.cache_data
def load_alarm_audio():

    for path in ALARM_CANDIDATES:

        if path.exists():
            return path.read_bytes(), ALARM_MIME

    return make_fallback_beep(), "audio/wav"


# =========================================================
# DROWSINESS VIDEO PROCESSOR
# =========================================================

class DrowsinessProcessor(VideoProcessorBase):

    def __init__(self, model, face_cascade):

        self.model = model
        self.face_cascade = face_cascade

        # User settings
        self.awake_min = 60.0
        self.alert_time = 2.0
        self.mirror = True
        self.analyze_every = 5

        # Detection state
        self.alarm = False
        self.awake_pct = None

        # Internal variables
        self.sleepy_start = None
        self.frame_count = 0

        self.box = None
        self.label_text = ""
        self.color = (0, 255, 0)

    def _analyze(self, img):

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80)
        )

        # No face detected
        if len(faces) == 0:

            self.box = None
            self.sleepy_start = None
            self.alarm = False
            self.awake_pct = None

            return

        # Select largest face
        x, y, w, h = max(
            faces,
            key=lambda f: f[2] * f[3]
        )

        face = cv2.resize(
            img[y:y + h, x:x + w],
            (64, 64)
        )

        face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        ).astype(np.float32)

        face = np.expand_dims(face, axis=0)

        # CNN prediction
        pred = float(
            self.model.predict(face, verbose=0)[0][0]
        )

        awake_pct = (1 - pred) * 100

        self.awake_pct = awake_pct

        sleepy = (
            pred >= 0.5
            or awake_pct < self.awake_min
        )

        if sleepy:

            if self.sleepy_start is None:
                self.sleepy_start = time.time()

            elapsed = (
                time.time() - self.sleepy_start
            )

            self.alarm = (
                elapsed >= self.alert_time
            )

            self.color = (0, 0, 255)

            self.label_text = (
                f"Sleepy ({awake_pct:.0f}% awake) "
                f"{elapsed:.1f}s"
            )

        else:

            self.sleepy_start = None
            self.alarm = False

            self.color = (0, 255, 0)

            self.label_text = (
                f"Awake ({awake_pct:.0f}%)"
            )

        self.box = (x, y, w, h)

        publish(
            "drowsiness",
            awake_pct=self.awake_pct,
            alarm=self.alarm
        )

    def _draw(self, img):

        if self.box is None:
            return

        x, y, w, h = self.box

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            self.color,
            2
        )

        cv2.putText(
            img,
            self.label_text,
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.color,
            2
        )

        if self.alarm:

            cv2.putText(
                img,
                "DROWSINESS ALERT!",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        if self.mirror:
            img = cv2.flip(img, 1)

        self.frame_count += 1

        if (
            self.frame_count
            % max(1, self.analyze_every)
            == 0
        ):
            self._analyze(img)

        self._draw(img)

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )


# =========================================================
# STREAMLIT PAGE
# =========================================================

def show_drowsiness():

    st.markdown(
        """
        <div class="main-title">
            Drowsiness Detection
        </div>

        <div class="page-subtitle">
            Real-time AI-based driver alertness monitoring
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load model and face detector
    try:

        model = load_drowsiness_model()
        face_cascade = load_face_detector()

    except Exception as e:

        st.error(
            "Unable to load the drowsiness detection system."
        )

        st.code(str(e))
        return

    # Model information
    c1, c2, c3 = st.columns(3)

    c1.metric("Model", "CNN")
    c2.metric("Input Size", "64 × 64")
    c3.metric("Detection", "Live Video")

    st.markdown("---")

    # -----------------------------------------------------
    # ALERT SETTINGS
    # -----------------------------------------------------

    st.markdown("### Alert Settings")

    awake_min = st.slider(
        "Sound the alarm when Awake % drops below",
        30,
        90,
        60
    )

    alert_time = st.slider(
        "Seconds of drowsiness before alarm",
        1.0,
        5.0,
        2.0,
        0.5
    )

    analyze_every = st.select_slider(
        "Performance (analyze every N frames)",
        options=[1, 2, 3, 4, 5],
        value=5,
        help="Higher values reduce CPU usage but may delay detection."
    )

    # -----------------------------------------------------
    # CAMERA SETTINGS
    # -----------------------------------------------------

    st.markdown("### Driver Monitoring")

    cam_col1, cam_col2 = st.columns(2)

    with cam_col1:

        camera_choice = st.radio(
            "Camera",
            ["Front camera", "Back camera"],
            horizontal=True
        )

    facing = (
        "user"
        if camera_choice == "Front camera"
        else "environment"
    )

    with cam_col2:

        mirror = st.checkbox(
            "Mirror view (flip)",
            value=(facing == "user"),
            key=f"mirror-{facing}"
        )

    st.info(
        "Click START, allow camera access, and keep your "
        "face clearly visible. To switch cameras, press "
        "STOP, change the option, and press START again."
    )

    # -----------------------------------------------------
    # WEBRTC CAMERA STREAM
    # -----------------------------------------------------

    ctx = webrtc_streamer(
        key=f"drowsiness-{facing}",

        video_processor_factory=lambda:
            DrowsinessProcessor(
                model,
                face_cascade
            ),

        rtc_configuration=get_rtc_config(),

        media_stream_constraints={
            "video": {
                "facingMode": {
                    "ideal": facing
                },
                "width": {
                    "ideal": 320
                },
                "height": {
                    "ideal": 240
                }
            },
            "audio": False
        },

        async_processing=True
    )

    # Load alarm
    audio_bytes, audio_mime = load_alarm_audio()

    # -----------------------------------------------------
    # LIVE STATUS
    # IMPORTANT: Keep this function INSIDE show_drowsiness
    # -----------------------------------------------------

    @st.fragment(run_every=0.5)
    def live_status():

        p = ctx.video_processor

        if not p:
            st.info("Start the camera to begin monitoring.")
            return

        # Update processor settings
        p.awake_min = awake_min
        p.alert_time = alert_time
        p.mirror = mirror
        p.analyze_every = analyze_every

        if not ctx.state.playing:
            st.info("Camera monitoring is stopped.")
            return

        if p.alarm:

            st.error(
                "🚨 DROWSINESS ALERT — Driver appears sleepy!"
            )

            st.audio(
                audio_bytes,
                format=audio_mime,
                loop=True
            )

        elif p.awake_pct is None:

            st.warning("No face detected.")

        else:

            st.success(
                f"Driver is awake ({p.awake_pct:.0f}%)"
            )

    live_status()
