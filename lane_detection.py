import streamlit as st
import cv2
import numpy as np


# =========================================================
# LANE DETECTION
# =========================================================

def detect_lanes(image):

    # -----------------------------------------------------
    # Resize for lower laptop load
    # -----------------------------------------------------

    height, width = image.shape[:2]

    new_width = 640
    new_height = int(height * new_width / width)

    image = cv2.resize(
        image,
        (new_width, new_height)
    )

    # -----------------------------------------------------
    # Grayscale
    # -----------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # -----------------------------------------------------
    # Gaussian Blur
    # -----------------------------------------------------

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # -----------------------------------------------------
    # Canny Edge Detection
    # -----------------------------------------------------

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    # -----------------------------------------------------
    # Region of Interest
    # -----------------------------------------------------

    h, w = edges.shape

    mask = np.zeros_like(edges)

    roi = np.array(
        [[
            (0, h),
            (int(0.40 * w), int(0.55 * h)),
            (int(0.60 * w), int(0.55 * h)),
            (w, h)
        ]],
        dtype=np.int32
    )

    cv2.fillPoly(
        mask,
        roi,
        255
    )

    cropped_edges = cv2.bitwise_and(
        edges,
        mask
    )

    # -----------------------------------------------------
    # Hough Line Detection
    # -----------------------------------------------------

    lines = cv2.HoughLinesP(
        cropped_edges,
        1,
        np.pi / 180,
        threshold=40,
        minLineLength=40,
        maxLineGap=100
    )

    left_lines = []
    right_lines = []

    if lines is not None:

        for line in lines:

            x1, y1, x2, y2 = line[0]

            if x2 == x1:
                continue

            slope = (y2 - y1) / (x2 - x1)

            # Ignore horizontal lines
            if abs(slope) < 0.5:
                continue

            if slope < 0:
                left_lines.append(
                    (x1, y1, x2, y2)
                )

            else:
                right_lines.append(
                    (x1, y1, x2, y2)
                )

    # -----------------------------------------------------
    # Draw detected lane
    # -----------------------------------------------------

    def draw_line(lines, color):

        if len(lines) == 0:
            return

        points_x = []
        points_y = []

        for x1, y1, x2, y2 in lines:

            points_x.extend(
                [x1, x2]
            )

            points_y.extend(
                [y1, y2]
            )

        if len(points_x) < 2:
            return

        slope, intercept = np.polyfit(
            points_x,
            points_y,
            1
        )

        y1 = h
        y2 = int(0.55 * h)

        if slope == 0:
            return

        x1 = int(
            (y1 - intercept) / slope
        )

        x2 = int(
            (y2 - intercept) / slope
        )

        cv2.line(
            image,
            (x1, y1),
            (x2, y2),
            color,
            7
        )

    # Left lane
    draw_line(
        left_lines,
        (255, 0, 0)
    )

    # Right lane
    draw_line(
        right_lines,
        (0, 255, 0)
    )

    # -----------------------------------------------------
    # Label
    # -----------------------------------------------------

    cv2.putText(
        image,
        "LANE DETECTION",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    return image


# =========================================================
# STREAMLIT PAGE
# =========================================================

def show_lane_detection():

    st.markdown(
        """
        <div class="main-title">
            Lane Detection
        </div>

        <div class="page-subtitle">
            Real-time road lane monitoring using computer vision
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # Feature Information
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Technology",
            "OpenCV"
        )

    with col2:
        st.metric(
            "Method",
            "Hough Lines"
        )

    with col3:
        st.metric(
            "Processing",
            "Real-time"
        )

    st.markdown("---")

    # -----------------------------------------------------
    # Image / Camera Input
    # -----------------------------------------------------

    st.markdown("### Road Analysis")

    input_mode = st.radio(
        "Select Input",
        [
            "Upload Road Image",
            "Use Camera"
        ],
        horizontal=True
    )

    # =====================================================
    # IMAGE MODE
    # =====================================================

    if input_mode == "Upload Road Image":

        uploaded_file = st.file_uploader(
            "Upload a road image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if uploaded_file is not None:

            file_bytes = np.asarray(
                bytearray(
                    uploaded_file.read()
                ),
                dtype=np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            result = detect_lanes(image)

            result_rgb = cv2.cvtColor(
                result,
                cv2.COLOR_BGR2RGB
            )

            st.image(
                result_rgb,
                caption="Lane Detection Result",
                use_container_width=True
            )

            st.success(
                "Lane detection completed."
            )

    # =====================================================
    # CAMERA MODE
    # =====================================================

    else:

        st.info(
            "Camera input will use your device camera."
        )

        camera_image = st.camera_input(
            "Capture road image"
        )

        if camera_image is not None:

            file_bytes = np.asarray(
                bytearray(
                    camera_image.read()
                ),
                dtype=np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            result = detect_lanes(image)

            result_rgb = cv2.cvtColor(
                result,
                cv2.COLOR_BGR2RGB
            )

            st.image(
                result_rgb,
                caption="Lane Detection Result",
                use_container_width=True
            )

            st.success(
                "Lane detection completed."
            )