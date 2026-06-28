import streamlit as st
import cv2
import numpy as np
from PIL import Image

def display_camera_feed(camera_type="Front"):
    """Display camera feed placeholder"""
    st.info(f"📷 {camera_type} Camera Feed")
    st.markdown(
        f"<div style='background-color: #222; padding: 20px; border-radius: 10px; text-align: center; color: white;'>"
        f"<p style='font-size: 48px;'>📷</p>"
        f"<p>{camera_type} Camera Stream</p>"
        f"<p style='color: #999; font-size: 12px;'>Connect actual camera source for live feed</p>"
        f"</div>",
        unsafe_allow_html=True
    )

def camera_selector():
    """Allow user to select camera source"""
    cameras = {
        "🚗 Front Camera": "front",
        "👤 Driver Camera": "driver",
        "🔙 Rear Camera": "rear",
        "🛣️ Road Camera": "road"
    }
    
    selected = st.radio("Select Camera", list(cameras.keys()), horizontal=True)
    return cameras[selected]

def display_detection_results(frame, detections):
    """Display frame with detection results"""
    st.image(frame, caption="Detection Results", use_column_width=True)
    
    if detections:
        st.subheader("Detected Objects")
        for detection in detections:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**{detection['label']}**")
            with col2:
                st.write(f"Confidence: {detection['confidence']:.2f}")
            with col3:
                st.write(f"Box: {detection['bbox']}")

def draw_bounding_boxes(image, detections):
    """Draw bounding boxes on image"""
    img = image.copy()
    
    for detection in detections:
        x1, y1, x2, y2 = detection['bbox']
        label = detection['label']
        confidence = detection['confidence']
        
        # Draw rectangle
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw label
        text = f"{label} ({confidence:.2f})"
        cv2.putText(img, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return img
