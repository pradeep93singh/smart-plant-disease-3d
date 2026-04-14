from fastapi import FastAPI, File, HTTPException, UploadFile

from app.iot import compute_environmental_risk, get_latest_sensor_state, update_sensor_state
from app.pipeline import run_analysis
from app.recommendations import build_recommendation
from app.schemas import DiseaseAnalysisResponse, ScanHistoryItem, SensorPayload
from app.storage import init_db, list_scans, save_scan

app = FastAPI(title="Smart Plant Disease Detection and Recommendation Platform")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/iot/sensor")
def ingest_sensor(payload: SensorPayload) -> dict:
    saved = update_sensor_state(payload)
    risk = compute_environmental_risk(saved)
    return {"message": "sensor data accepted", "risk": risk}


@app.get("/history", response_model=list[ScanHistoryItem])
def history(limit: int = 20) -> list[ScanHistoryItem]:
    records = list_scans(limit=limit)
    return [
        ScanHistoryItem(
            id=record.id or 0,
            plant_name=record.plant_name,
            disease_name=record.disease_name,
            confidence_score=record.confidence_score,
            severity_percentage=record.severity_percentage,
            urgency_level=record.urgency_level,
            created_at=record.created_at,
        )
        for record in records
    ]


@app.post("/analyze", response_model=DiseaseAnalysisResponse)
async def analyze_leaf_image(image: UploadFile = File(...)) -> DiseaseAnalysisResponse:
    if not image.content_type or "image" not in image.content_type:
        raise HTTPException(status_code=400, detail="Please upload a valid image file.")
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    analysis = run_analysis(image_bytes)
    recommendation = build_recommendation(analysis["disease_name"], analysis["severity_percentage"])
    sensor_state = get_latest_sensor_state()
    env_risk = compute_environmental_risk(sensor_state)

    result = DiseaseAnalysisResponse(
        plant_name=analysis["plant_name"],
        disease_name=analysis["disease_name"],
        disease_type=recommendation["disease_type"],
        confidence_score=analysis["confidence_score"],
        severity_percentage=analysis["severity_percentage"],
        severity_level=recommendation["severity_level"],
        affected_region_image_b64=analysis["affected_region_image_b64"],
        explainability_heatmap_b64=analysis["explainability_heatmap_b64"],
        symptoms=recommendation["symptoms"],
        causes=recommendation["causes"],
        recommended_solution=recommendation["recommended_solution"],
        prevention_tips=recommendation["prevention_tips"],
        urgency_level=recommendation["urgency_level"],
        yield_risk=recommendation["yield_risk"],
        iot_risk_flag=env_risk["risk_flag"] if env_risk else None,
        environmental_snapshot=env_risk,
    )

    save_scan(
        plant_name=result.plant_name,
        disease_name=result.disease_name,
        confidence_score=result.confidence_score,
        severity_percentage=result.severity_percentage,
        urgency_level=result.urgency_level,
    )
    return result
