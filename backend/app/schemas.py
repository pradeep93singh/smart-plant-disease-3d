from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SensorPayload(BaseModel):
    temperature_c: float
    humidity_pct: float
    soil_moisture_pct: float
    captured_at: datetime = Field(default_factory=datetime.utcnow)


class DiseaseAnalysisResponse(BaseModel):
    plant_name: str
    disease_name: str
    disease_type: str
    confidence_score: float
    severity_percentage: float
    severity_level: str
    affected_region_image_b64: str
    explainability_heatmap_b64: str
    symptoms: List[str]
    causes: List[str]
    recommended_solution: List[str]
    prevention_tips: List[str]
    urgency_level: str
    yield_risk: str
    iot_risk_flag: Optional[str] = None
    environmental_snapshot: Optional[Dict[str, float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScanHistoryItem(BaseModel):
    id: int
    plant_name: str
    disease_name: str
    confidence_score: float
    severity_percentage: float
    urgency_level: str
    created_at: datetime
