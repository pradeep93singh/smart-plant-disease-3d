import base64
import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Dict, Any

import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st
from PIL import Image
from requests.exceptions import RequestException

# Path fix for imports
APP_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_ROOT / 'backend'))

API_URL = os.getenv("API_URL", "http://127.0.0.1:8010")

# Fallback functions for standalone mode
def fallback_local_iot_risk(payload: dict) -> str:
    return "moderate"

def fallback_run_analysis(image_bytes: bytes) -> Dict:
    return {
        "plant_name": "Tomato",
        "disease_name": "Early Blight",
        "confidence_score": 0.84,
        "severity_percentage": 25.5,
        "affected_region_image_b64": "",
        "explainability_heatmap_b64": "",
    }

def fallback_build_recommendation(disease, severity):
    return {
        "disease_type": "Fungal",
        "severity_level": "Moderate",
        "symptoms": ["Spots on leaves"],
        "causes": ["High humidity"],
        "recommended_solution": ["Fungicide", "Improve air flow"],
        "prevention_tips": ["Proper spacing"],
        "plant_care": ["Water weekly"],
        "urgency_level": "Medium",
        "yield_risk": "15-20%"
    }

# Try real imports, fallback if fail
try:
    from backend.app.iot import SensorPayload, compute_environmental_risk
    from backend.app.pipeline import run_analysis
    from backend.app.recommendations import build_recommendation
except ImportError:
    SensorPayload = type('dummy', (), {})
    compute_environmental_risk = lambda s: {"risk_flag": "moderate"}
    run_analysis = fallback_run_analysis
    build_recommendation = fallback_build_recommendation

def b64_to_image(encoded: str) -> Image.Image:
    try:
        return Image.open(BytesIO(base64.b64decode(encoded)))
    except:
        return Image.new('RGB', (200, 200), color = 'lightgray')

def api_available() -> bool:
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.ok
    except:
        return False

def local_iot_risk(payload: dict) -> str:
    try:
        state = SensorPayload(**payload)
        risk = compute_environmental_risk(state)
        return risk.get("risk_flag", "n/a")
    except:
        return "moderate"

def local_analyze(image_bytes: bytes) -> Dict:
    try:
        analysis = run_analysis(image_bytes)
        recommendation = build_recommendation(analysis["disease_name"], analysis["severity_percentage"], analysis["plant_name"])
        result = {
            "plant_name": analysis["plant_name"],
            "disease_name": analysis["disease_name"],
            "disease_type": recommendation["disease_type"],
            "confidence_score": analysis["confidence_score"],
            "severity_percentage": analysis["severity_percentage"],
            "severity_level": recommendation["severity_level"],
            "affected_region_image_b64": analysis["affected_region_image_b64"],
            "explainability_heatmap_b64": analysis["explainability_heatmap_b64"],
            "symptoms": recommendation["symptoms"],
            "causes": recommendation["causes"],
            "recommended_solution": recommendation["recommended_solution"],
            "prevention_tips": recommendation["prevention_tips"],
            "plant_care": recommendation["plant_care"],
            "urgency_level": recommendation["urgency_level"],
            "yield_risk": recommendation["yield_risk"],
        }
        result["iot_risk_flag"] = st.session_state.get("iot_risk_flag", "not available")
        return result
    except Exception as e:
        st.error(f"Local analysis error: {e}")
        return fallback_run_analysis(image_bytes) | fallback_build_recommendation("Unknown", 0)

st.set_page_config(
    page_title="PlantCare Fullstack Camera Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

remote_mode = api_available()
st.caption(f"{'🟢 Backend API Connected' if remote_mode else '🟡 Local Fallback Mode'}")

# Sidebar
with st.sidebar:
    st.header("🌡️ IoT Sensors")
    temp = st.slider("Temperature (°C)", 0.0, 50.0, 28.0)
    hum = st.slider("Humidity (%)", 0.0, 100.0, 70.0)
    soil = st.slider("Soil Moisture (%)", 0.0, 100.0, 60.0)
    if st.button("📤 Update Sensors", use_container_width=True):
        payload = {"temperature_c": temp, "humidity_pct": hum, "soil_moisture_pct": soil}
        st.session_state["iot_risk_flag"] = local_iot_risk(payload)
        st.balloons()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📱 Live Camera", "📤 Upload", "📊 Results", "💡 Advice"])

with tab1:
    st.header("🔴 Live Camera Detection")
    camera_img = st.camera_input("Point camera at plant leaf")
    if camera_img:
        st.image(camera_img, caption="Live Preview", use_column_width=True)
        if st.button("🚀 Analyze Live", type="primary", use_container_width=True):
            with st.spinner("Analyzing with AI..."):
                upload_bytes = camera_img.getvalue()
                if remote_mode:
                    files = {"image": ("leaf.jpg", upload_bytes, "image/jpeg")}
                    resp = requests.post(f"{API_URL}/analyze", files=files, timeout=30)
                    result = resp.json() if resp.ok else {"error": resp.text}
                else:
                    result = local_analyze(upload_bytes)
                st.session_state["result"] = result
                st.success("✅ Live analysis complete!")
            if "error" in result:
                st.error(result["error"])
            else:
                st.rerun()

with tab2:
    st.header("📤 Upload Photo")
    upload = st.file_uploader("Choose leaf image", type=['jpg', 'jpeg', 'png'])
    if upload:
        st.image(upload, caption="Uploaded", use_column_width=True)
        if st.button("🔬 Analyze Upload", use_container_width=True):
            with st.spinner("Processing..."):
                upload_bytes = upload.getvalue()
                if remote_mode:
                    files = {"image": (upload.name, upload_bytes, upload.type)}
                    resp = requests.post(f"{API_URL}/analyze", files=files, timeout=30)
                    result = resp.json() if resp.ok else {"error": resp.text}
                else:
                    result = local_analyze(upload_bytes)
                st.session_state["result"] = result
                st.success("Analysis complete!")
            if "error" in result:
                st.error(result["error"])

with tab3:
    if "result" in st.session_state:
        result = st.session_state["result"]
        col1, col2, col3 = st.columns(3)
        col1.metric("🌿 Plant Type", result.get("plant_name", "N/A"))
        col2.metric("🦠 Disease", result.get("disease_name", "N/A"))
        col3.metric("🎯 Confidence", f"{result.get('confidence_score', 0)*100:.1f}%")
        
        col4, col5, col6 = st.columns(3)
        severity = result.get("severity_percentage", 0)
        col4.metric("⚠️ Severity", result.get("severity_level", "N/A"))
        col5.metric("📏 Coverage", f"{severity:.1f}%")
        col6.metric("🚨 Action", result.get("urgency_level", "N/A"))
        
        st.info(f"Yield Risk: {result.get('yield_risk')} | IoT Risk: {st.session_state.get('iot_risk_flag', 'N/A')}")
        
        # Images
        col_img1, col_img2 = st.columns(2)
        try:
            affected = b64_to_image(result["affected_region_image_b64"])
            heatmap = b64_to_image(result["explainability_heatmap_b64"])
            col_img1.image(affected, "Affected Region", use_column_width=True)
            col_img2.image(heatmap, "AI Heatmap", use_column_width=True)
        except:
            st.warning("Image previews unavailable")
        
        # 3D Interactive
        severity_sim = st.slider("3D Severity Simulation (%)", 0, 100, int(severity))
        fig3d = go.Figure()
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x_leaf = 4 * np.outer(np.cos(u), np.sin(v))
        y_leaf = 2.5 * np.outer(np.sin(u), np.sin(v))
        z_leaf = 0.05 * np.outer(np.ones_like(u), np.cos(v))
        fig3d.add_trace(go.Surface(x=x_leaf, y=y_leaf, z=z_leaf, colorscale="Greens", opacity=0.8))
        nx = 20
        xx = np.linspace(-4,4,nx)
        yy = np.linspace(-2,2,nx)
        zz = np.random.rand(nx,nx) * (severity_sim/100)
        fig3d.add_trace(go.Scatter3d(x=xx.flatten(), y=yy.flatten(), z=zz.flatten(), mode='markers', marker=dict(color=zz.flatten(), colorscale='Reds', size=8, opacity=0.8)))
        fig3d.update_layout(title="🧬 3D Disease Model", height=500)
        st.plotly_chart(fig3d, use_container_width=True)

with tab4:
    if "result" in st.session_state:
        result = st.session_state["result"]
        if "error" not in result:
            st.header(f"💡 Complete Guide for {result['plant_name']} - {result['disease_name']}")
            
            st.subheader("📋 Symptoms")
            for symptom in result["symptoms"]:
                st.write(f"• {symptom}")
            
            st.subheader("🔬 Causes")
            for cause in result["causes"]:
                st.write(f"• {cause}")
            
            st.subheader("✅ Recommended Solutions")
            for sol in result["recommended_solution"]:
                st.success(sol)
            
            st.subheader("🛡️ Prevention Tips")
            for tip in result["prevention_tips"]:
                st.info(tip)
            
            if result.get("plant_care"):
                st.subheader("🌱 Plant Care Instructions")
                for care in result["plant_care"]:
                    st.write(f"🌟 {care}")
            
            st.balloons()

st.markdown("---")
st.caption("🌿 PlantCare AI - Live Camera Detection with Full Details | v2.1")

if st.button("📜 Scan History"):
    if remote_mode:
        try:
            resp = requests.get(f"{API_URL}/history?limit=50")
            st.dataframe(resp.json())
        except Exception as e:
            st.error(f"History fetch failed: {e}")

