import streamlit as st

def render_sidebar():
    """Render the main sidebar navigation"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150", width=150)
        st.markdown("# 🚗 DriveSense AI")
        st.markdown("Smart Vehicle Monitoring System")
        st.divider()
        
        # Navigation menu
        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "🚗 Vehicle Health",
                "🛠 Maintenance",
                "👤 Driver Monitoring",
                "🚦 Traffic Signs",
                "📷 Live Cameras",
                "🔔 Alerts",
                "📄 Reports",
                "⚙ Settings"
            ]
        )
        
        st.divider()
        
        # Quick stats
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Vehicles", "5", "Online")
        with col2:
            st.metric("Alerts", "24", "+3 today")
        
        st.divider()
        
        # System status
        st.markdown("### ⚡ System Status")
        st.success("✅ All Systems Operational")
        
        st.divider()
        
        # About section
        st.markdown("### ℹ️ About")
        st.info(
            "DriveSense AI is an intelligent vehicle monitoring platform "
            "that combines AI, ML, and Computer Vision for safer roads."
        )
        
        return page
