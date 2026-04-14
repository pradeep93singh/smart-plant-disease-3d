import base64
import os
import sys
from io import BytesIO
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st
from PIL import Image
from requests.exceptions import RequestException

API_URL = os.getenv("API_URL", "http://127.0.0.1:8010")
APP_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = APP_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

from app.iot import SensorPayload, compute_environmental_risk  # noqa: E402
from app.pipeline import run_analysis  # noqa: E402
from app.recommendations import build_recommendation  # noqa: E402


def b64_to_image(encoded: str) -> Image.Image:
    return Image.open(BytesIO(base64.b64decode(encoded)))


def build_3d_leaf_surface(image: Image.Image, title: str) -> go.Figure:
    grayscale = np.array(image.convert("L"))
    if grayscale.shape[0] > 180 or grayscale.shape[1] > 180:
        grayscale = grayscale[::3, ::3]
    z = grayscale.astype(np.float32) / 255.0
    y = np.arange(z.shape[0])
    x = np.arange(z.shape[1])
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale="YlGn", showscale=True)])
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="Leaf Width",
            yaxis_title="Leaf Height",
            zaxis_title="Infection Intensity",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        height=460,
    )
    return fig


def api_available() -> bool:
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.ok
    except RequestException:
        return False


def local_iot_risk(payload: dict) -> str:
    state = SensorPayload(**payload)
    risk = compute_environmental_risk(state)
    return risk["risk_flag"] if risk else "n/a"


def local_analyze(image_bytes: bytes) -> dict:
    analysis = run_analysis(image_bytes)
    recommendation = build_recommendation(analysis["disease_name"], analysis["severity_percentage"])
    return {
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
        "urgency_level": recommendation["urgency_level"],
        "yield_risk": recommendation["yield_risk"],
        "iot_risk_flag": st.session_state.get("iot_risk_flag", "not available"),
    }


st.set_page_config(page_title="Smart Plant Disease Platform", layout="wide")
st.title("Smart Plant Disease Detection and Recommendation Platform")
remote_mode = api_available()
st.caption(
    f"Mode: {'Remote API' if remote_mode else 'Standalone Streamlit (no backend required)'}"
)

with st.sidebar:
    st.header("IoT Sensor Snapshot (Optional)")
    temp = st.slider("Temperature (C)", min_value=0.0, max_value=50.0, value=28.0)
    hum = st.slider("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
    soil = st.slider("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=60.0)
    if st.button("Send IoT Data"):
        payload = {"temperature_c": temp, "humidity_pct": hum, "soil_moisture_pct": soil}
        if remote_mode:
            try:
                response = requests.post(f"{API_URL}/iot/sensor", json=payload, timeout=15)
                if response.ok:
                    iot_flag = response.json().get("risk", {}).get("risk_flag", "n/a")
                    st.session_state["iot_risk_flag"] = iot_flag
                    st.success(f"IoT risk: {iot_flag}")
                else:
                    st.error("Failed to send IoT data")
            except RequestException:
                st.error("IoT request failed.")
        else:
            iot_flag = local_iot_risk(payload)
            st.session_state["iot_risk_flag"] = iot_flag
            st.success(f"IoT risk: {iot_flag}")

upload = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png"])

if upload and st.button("Analyze Leaf"):
    upload_bytes = upload.getvalue()
    if remote_mode:
        files = {"image": (upload.name, upload_bytes, upload.type)}
        response = requests.post(f"{API_URL}/analyze", files=files, timeout=90)
        if not response.ok:
            st.error(f"Analysis failed: {response.text}")
            st.stop()
        result = response.json()
    else:
        result = local_analyze(upload_bytes)

    st.subheader("Prediction Output")
    col1, col2, col3 = st.columns(3)
    col1.metric("Plant", result["plant_name"])
    col2.metric("Disease", result["disease_name"])
    col3.metric("Confidence", f"{result['confidence_score']*100:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Severity", result["severity_level"])
    col5.metric("Affected Area", f"{result['severity_percentage']:.2f}%")
    col6.metric("Urgency", result["urgency_level"])

    st.write(f"**Disease Type:** {result['disease_type']}")
    st.write(f"**Yield Risk:** {result['yield_risk']}")
    st.write(f"**IoT Risk Flag:** {result.get('iot_risk_flag', 'not available')}")

    img_col1, img_col2 = st.columns(2)
    affected_img = b64_to_image(result["affected_region_image_b64"])
    heatmap_img = b64_to_image(result["explainability_heatmap_b64"])
    img_col1.image(affected_img, caption="Affected Region Visualization")
    img_col2.image(heatmap_img, caption="Explainability Heatmap")

    st.markdown("### 3D Lesion and Severity View")
    plot_col1, plot_col2 = st.columns(2)
    plot_col1.plotly_chart(
        build_3d_leaf_surface(affected_img, "3D Infected Region Surface"),
        use_container_width=True,
    )
    plot_col2.plotly_chart(
        build_3d_leaf_surface(heatmap_img, "3D Explainability Surface"),
        use_container_width=True,
    )

    st.markdown("### Symptoms")
    st.write(", ".join(result["symptoms"]))

    st.markdown("### Causes")
    st.write(", ".join(result["causes"]))

    st.markdown("### Recommended Solution")
    for item in result["recommended_solution"]:
        st.write(f"- {item}")

    st.markdown("### Prevention Tips")
    for item in result["prevention_tips"]:
        st.write(f"- {item}")

st.markdown("---")
if st.button("Load Scan History"):
    if remote_mode:
        response = requests.get(f"{API_URL}/history", timeout=15)
        if response.ok:
            st.dataframe(response.json(), use_container_width=True)
        else:
            st.error("Unable to fetch history.")
    else:
        st.info("Scan history is available in remote API mode.")
