import streamlit as st
import base64
from io import BytesIO
from pathlib import Path
import sys
import numpy as np
from PIL import Image
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="PlantCare Fullstack",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fullstack theme
st.markdown("""
<style>
.main { background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #3730a3 100%); }
.stApp { background: transparent; }
.sidebar .sidebar-content { background: rgba(30,58,138,0.95); }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 20px; margin-bottom: 2rem; backdrop-filter: blur(20px);'>
    <h1 style='color: white; font-size: 3.5rem; margin-bottom: 0.5rem; text-shadow: 0 4px 8px rgba(0,0,0,0.5);'>
        🌿 PlantCare Fullstack AI
    </h1>
    <p style='color: #bfdbfe; font-size: 1.3rem;'>Camera Scan • 3D Detection • ML Training • Backend Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🚀 Control Panel")
page = st.sidebar.selectbox("Select Mode", [
    "📱 Live Camera Scan", 
    "🧬 3D Disease Model", 
    "📊 Backend Dashboard", 
    "🎓 ML Training", 
    "📈 IoT Sensors"
])

# Global session state
if 'result' not in st.session_state:
    st.session_state.result = {}
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []

# Page 1: Live Camera Scan
if page == "📱 Live Camera Scan":
    st.header("🔍 Live Plant Scanner")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📸 Camera View")
        camera_col1, camera_col2 = st.columns(2)
        with camera_col1:
            # Mock camera
            st.image("https://images.unsplash.com/photo-1612872087726-dda829ec1714?w=300", caption="Live Feed")
        with camera_col2:
            if st.button("🎯 SCAN DISEASE", use_container_width=True):
                st.session_state.result = {
                    "plant": "Tomato",
                    "disease": "Early Blight",
                    "confidence": 94.2,
                    "severity": 27.8,
                    "treatment": "Fungicide spray"
                }
                st.success("✅ Analysis complete!")
        
        st.markdown("### Detection Marks")
        st.image("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjNmM2YzIi8+Cg==", use_container_width=True)

    with col2:
        st.markdown("### 📋 Results")
        if st.session_state.result:
            st.metric("🌱 Plant", st.session_state.result["plant"])
            st.metric("🦠 Disease", st.session_state.result["disease"])
            st.metric("🎯 Accuracy", f"{st.session_state.result['confidence']}%")
            st.metric("⚠️ Severity", f"{st.session_state.result['severity']}%")
            
            st.success(st.session_state.result["treatment"])

# Page 2: 3D Model
elif page == "🧬 3D Disease Model":
    st.header("🧬 Interactive 3D Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        severity_slider = st.slider("Disease Progression", 0.0, 100.0, 30.0)
        
        # 3D Plot
        fig = go.Figure()
        # Leaf surface
        x_leaf = np.linspace(-3, 3, 50)
        y_leaf = np.linspace(-2, 2, 30)
        X_leaf, Y_leaf = np.meshgrid(x_leaf, y_leaf)
        Z_leaf = np.sin(np.sqrt(X_leaf**2 + Y_leaf**2)) * 0.3
        
        fig.add_trace(go.Surface(x=X_leaf, y=Y_leaf, z=Z_leaf, colorscale="Greens", opacity=0.8))
        
        # Lesions
        lesions_x = np.random.uniform(-2.5, 2.5, 25)
        lesions_y = np.random.uniform(-1.5, 1.5, 25)
        lesions_z = severity_slider / 100 * np.random.uniform(0.1, 0.5, 25)
        fig.add_trace(go.Scatter3d(x=lesions_x, y=lesions_y, z=lesions_z, mode='markers', marker=dict(size=8, color='red', opacity=0.8)))
        
        fig.update_layout(height=600, scene=dict(aspectmode="data"))
        st.plotly_chart(fig, use_container_width=True)

# Page 3: Backend Dashboard  
elif page == "📊 Backend Dashboard":
    st.header("📊 Backend Admin")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Metrics")
        col11, col12, col13 = st.columns(3)
        col11.metric("Scans", "1,247", "12%")
        col12.metric("Accuracy", "96.8%", "0.2%")
        col13.metric("Alerts", "23", "3")
    
    with col2:
        st.subheader("Model Status")
        st.success("✅ Live")
        st.info("GPU Usage: 45%")
        st.button("🔄 Retrain Model", use_container_width=True)

# Page 4: ML Training
elif page == "🎓 ML Training":
    st.header("🎓 Model Training Center")
    
    uploaded_files = st.file_uploader("Upload Dataset ZIP", accept_multiple_files=True, type="zip")
    
    if st.button("🚀 Start Training", use_container_width=True):
        with st.spinner("Training on GPU..."):
            st.success("Training complete! Accuracy improved 3.2%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Training Time", "45 min")
        st.metric("New Accuracy", "97.1%")
    with col2:
        st.metric("Dataset Size", "12,847 images")

# Page 5: IoT
elif page == "📈 IoT Sensors":
    st.header("🌡️ IoT Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🌡️ Temperature", "28.4°C", "0.2°C")
    with col2:
        st.metric("💧 Humidity", "72%", "+2%")
    with col3:
        st.metric("🌱 Soil Moisture", "65%", "-1%")
    
    st.subheader("Risk Assessment")
    st.progress(0.4)
    st.success("Moderate Risk")

st.markdown("---")
st.markdown("*Fullstack Plant Disease Detection Platform v2.0*")

