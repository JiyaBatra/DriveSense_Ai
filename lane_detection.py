import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

from signals import publish


# =========================================================
# CONFIG
# =========================================================

def get_rtc_config():
    """STUN always; TURN too if [turn] is set in .streamlit/secrets.toml."""
    servers = [{"urls": ["stun:stun.l.google.com:19302"]}]
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
# LANE DETECTOR (with smoothing for live video)
# =========================================================

class LaneDetector:
    def __init__(self, smoothing=0.8, max_missed=10, publish_signal=False):
        self.publish_signal = publish_signal   # True only for the live camera
        self.smoothing = smoothing             # higher = steadier lines
        self.max_missed = max_missed           # frames to keep a lane after it disappears
        self.left_fit = None
        self.right_fit = None
        self.left_missed = 0
        self.right_missed = 0

    @staticmethod
    def _fit(lines):
        """Average a group of line segments into one (slope, intercept)."""
        if len(lines) == 0:
            return None
        xs, ys = [], []
        for x1, y1, x2, y2 in lines:
            xs.extend([x1, x2])
            ys.extend([y1, y2])
        if len(xs) < 2 or len(set(xs)) < 2:
            return None
        slope, intercept = np.polyfit(xs, ys, 1)
        if slope == 0:
            return None
        return slope, intercept

    def _update(self, old, new, missed):
        """Blend new fit with the old one; keep old for a few missed frames."""
        if new is None:
            missed += 1
            if missed > self.max_missed:
                return None, missed
            return old, missed
        if old is None:
            return new, 0
        a = self.smoothing
        blended = (a * old[0] + (1 - a) * new[0],
                   a * old[1] + (1 - a) * new[1])
        return blended, 0

    @staticmethod
    def _points(fit, h, y_top):
        slope, intercept = fit
        x_bottom = int((h - intercept) / slope)
        x_top = int((y_top - intercept) / slope)
        return (x_bottom, h), (x_top, y_top)

    def detect(self, image):
        # Resize for lower load
        height, width = image.shape[:2]
        new_width = 640
        new_height = int(height * new_width / width)
        image = cv2.resize(image, (new_width, new_height))

        # Grayscale -> blur -> edges
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        # Region of interest
        h, w = edges.shape
        mask = np.zeros_like(edges)
        roi = np.array([[
            (0, h),
            (int(0.40 * w), int(0.55 * h)),
            (int(0.60 * w), int(0.55 * h)),
            (w, h),
        ]], dtype=np.int32)
        cv2.fillPoly(mask, roi, 255)
        cropped_edges = cv2.bitwise_and(edges, mask)

        # Hough lines
        lines = cv2.HoughLinesP(
            cropped_edges, 1, np.pi / 180,
            threshold=40, minLineLength=40, maxLineGap=100,
        )

        left_lines, right_lines = [], []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 == x1:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.5:      # ignore near-horizontal lines
                    continue
                if slope < 0:
                    left_lines.append((x1, y1, x2, y2))
                else:
                    right_lines.append((x1, y1, x2, y2))

        # Smooth over time
        self.left_fit, self.left_missed = self._update(
            self.left_fit, self._fit(left_lines), self.left_missed
        )
        self.right_fit, self.right_missed = self._update(
            self.right_fit, self._fit(right_lines), self.right_missed
        )

        # Draw
        y_top = int(0.55 * h)
        left_pts = right_pts = None

        if self.left_fit is not None:
            left_pts = self._points(self.left_fit, h, y_top)
            cv2.line(image, left_pts[0], left_pts[1], (255, 0, 0), 7)

        if self.right_fit is not None:
            right_pts = self._points(self.right_fit, h, y_top)
            cv2.line(image, right_pts[0], right_pts[1], (0, 255, 0), 7)

        # Light fill between the two lanes
        if left_pts and right_pts:
            overlay = image.copy()
            poly = np.array(
                [left_pts[0], left_pts[1], right_pts[1], right_pts[0]],
                dtype=np.int32,
            )
            cv2.fillPoly(overlay, [poly], (0, 255, 255))
            image = cv2.addWeighted(overlay, 0.25, image, 0.75, 0)

        status = (
            "BOTH LANES" if (left_pts and right_pts)
            else "ONE LANE" if (left_pts or right_pts)
            else "NO LANE"
        )

        # Vehicle offset from lane centre, as a fraction of lane width.
        # Negative = vehicle is left of centre, positive = right of centre.
        offset = None
        if left_pts and right_pts:
            lane_w = right_pts[0][0] - left_pts[0][0]
            if lane_w > 0:
                lane_center = (left_pts[0][0] + right_pts[0][0]) / 2
                offset = max(-1.0, min(1.0, (w / 2 - lane_center) / lane_w))

        label = f"LANE DETECTION - {status}"
        if offset is not None:
            label += f" | offset {offset:+.2f}"
        cv2.putText(image, label, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Send the result to the Accident Risk module
        if self.publish_signal:
            publish("lane", status=status, offset=offset)

        return image


# =========================================================
# VIDEO PROCESSOR (live camera)
# =========================================================

class LaneProcessor(VideoProcessorBase):
    def __init__(self):
        self.detector = LaneDetector(publish_signal=True)
        self.mirror = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        if self.mirror:
            img = cv2.flip(img, 1)
        result = self.detector.detect(img)
        return av.VideoFrame.from_ndarray(result, format="bgr24")


# =========================================================
# HELPERS
# =========================================================

def decode_upload(uploaded):
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)


# =========================================================
# STREAMLIT PAGE
# =========================================================

def show_lane_detection():
    st.markdown(
        """
        <div class="main-title">Lane Detection</div>
        <div class="page-subtitle">Real-time road lane monitoring using computer vision</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Technology", "OpenCV")
    c2.metric("Method", "Hough Lines")
    c3.metric("Processing", "Real-time")
    st.markdown("---")

    st.markdown("### Road Analysis")
    input_mode = st.radio(
        "Select Input",
        ["Live Camera", "Upload Road Image"],
        horizontal=True,
    )

    # ---------------- Upload mode ----------------
    if input_mode == "Upload Road Image":
        uploaded_file = st.file_uploader(
            "Upload a road image", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            image = decode_upload(uploaded_file)
            if image is None:
                st.error("Unable to read this image.")
                return

            # fresh detector, no smoothing carry-over, and no signal published
            result = LaneDetector().detect(image)
            st.image(
                cv2.cvtColor(result, cv2.COLOR_BGR2RGB),
                caption="Lane Detection Result",
                use_container_width=True,
            )
            st.success("Lane detection completed.")
        return

    # ---------------- Live camera mode ----------------
    cam_col1, cam_col2 = st.columns(2)
    with cam_col1:
        camera_choice = st.radio(
            "Camera", ["Back camera", "Front camera"], horizontal=True
        )
    facing = "environment" if camera_choice == "Back camera" else "user"

    with cam_col2:
        mirror = st.checkbox(
            "Mirror view (flip)",
            value=False,
            key=f"lane-mirror-{facing}",
            help="Usually keep this off for road view, mirroring swaps left and right.",
        )

    st.info(
        "Click START and allow camera access. "
        "To switch cameras: press STOP, change the option, then press START."
    )

    ctx = webrtc_streamer(
        key=f"lane-{facing}",  # new key restarts the stream with the chosen camera
        video_processor_factory=LaneProcessor,
        rtc_configuration=get_rtc_config(),
        media_stream_constraints={
            "video": {
                "facingMode": {"ideal": facing},
                "width": {"ideal": 640},
                "height": {"ideal": 480},
            },
            "audio": False,
        },
        async_processing=True,
    )

    # Push the mirror setting to the running processor
    if ctx.video_processor:
        ctx.video_processor.mirror = mirror