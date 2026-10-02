import streamlit as st
import tensorflow as tf
import cv2
import numpy as np


MODEL_PATH = "drowsiness_model.keras"


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_drowsiness_model():
    return tf.keras.models.load_model(MODEL_PATH)


# =========================================================
# LOAD FACE DETECTOR
# =========================================================

@st.cache_resource
def load_face_detector():

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    return face_cascade


# =========================================================
# DROWSINESS PAGE
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

    # -----------------------------------------------------
    # LOAD MODEL
    # -----------------------------------------------------

    try:

        model = load_drowsiness_model()
        face_cascade = load_face_detector()

    except Exception as e:

        st.error(
            "Unable to load the drowsiness detection system."
        )

        st.code(str(e))

        return

    # -----------------------------------------------------
    # MODEL INFORMATION
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model",
            "CNN"
        )

    with col2:
        st.metric(
            "Input Size",
            "64 × 64"
        )

    with col3:
        st.metric(
            "Detection",
            "AI Vision"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # CAMERA INPUT
    # -----------------------------------------------------

    st.markdown("### Driver Monitoring")

    st.info(
        "Allow camera access and keep your face clearly visible."
    )

    camera = st.camera_input(
        "Capture Driver Image"
    )

    if camera is None:
        return

    # -----------------------------------------------------
    # READ IMAGE
    # -----------------------------------------------------

    file_bytes = np.asarray(
        bytearray(camera.read()),
        dtype=np.uint8
    )

    frame = cv2.imdecode(
        file_bytes,
        cv2.IMREAD_COLOR
    )

    if frame is None:

        st.error(
            "Unable to read camera image."
        )

        return

    # -----------------------------------------------------
    # FACE DETECTION
    # -----------------------------------------------------

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    # -----------------------------------------------------
    # NO FACE
    # -----------------------------------------------------

    if len(faces) == 0:

        st.warning(
            "No face detected. Please capture another image."
        )

        st.image(
            cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )
        )

        return

    # -----------------------------------------------------
    # FIRST DETECTED FACE
    # -----------------------------------------------------

    x, y, w, h = faces[0]

    # Draw face rectangle
    cv2.rectangle(
        frame,
        (x, y),
        (x + w, y + h),
        (255, 0, 0),
        2
    )

    # -----------------------------------------------------
    # CROP FACE
    # -----------------------------------------------------

    face = frame[
        y:y + h,
        x:x + w
    ]

    face = cv2.resize(
        face,
        (64, 64)
    )

    # BGR → RGB
    face = cv2.cvtColor(
        face,
        cv2.COLOR_BGR2RGB
    )

    face = np.array(
        face,
        dtype=np.float32
    )

    # Add batch dimension
    face = np.expand_dims(
        face,
        axis=0
    )

    # -----------------------------------------------------
    # MODEL PREDICTION
    # -----------------------------------------------------

    prediction = model.predict(
        face,
        verbose=0
    )[0][0]

    # -----------------------------------------------------
    # CLASSIFICATION
    # -----------------------------------------------------

    if prediction >= 0.5:

        label = "Sleepy"
        confidence = prediction

    else:

        label = "Awake"
        confidence = 1 - prediction

    # -----------------------------------------------------
    # DISPLAY IMAGE
    # -----------------------------------------------------

    st.image(
        cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        ),
        caption="Driver Analysis",
        use_container_width=True
    )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    st.markdown("### Detection Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.metric(
            "Driver Status",
            label
        )

    with result_col2:

        st.metric(
            "Confidence",
            f"{confidence * 100:.1f}%"
        )

    # -----------------------------------------------------
    # ALERT
    # -----------------------------------------------------

    if label == "Sleepy":

        st.error(
            "DROWSINESS ALERT — Driver appears sleepy."
        )

    else:

        st.success(
            "Driver appears awake and attentive."
        )