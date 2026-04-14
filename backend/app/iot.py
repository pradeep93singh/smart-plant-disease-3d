from typing import Dict, Optional

from app.schemas import SensorPayload


_latest_sensor_state: Optional[SensorPayload] = None


def update_sensor_state(payload: SensorPayload) -> SensorPayload:
    global _latest_sensor_state
    _latest_sensor_state = payload
    return _latest_sensor_state


def get_latest_sensor_state() -> Optional[SensorPayload]:
    return _latest_sensor_state


def compute_environmental_risk(payload: Optional[SensorPayload]) -> Optional[Dict[str, float | str]]:
    if payload is None:
        return None

    score = 0.0
    if payload.humidity_pct > 75:
        score += 0.45
    if 22 <= payload.temperature_c <= 32:
        score += 0.35
    if payload.soil_moisture_pct > 65:
        score += 0.20

    if score < 0.3:
        flag = "low"
    elif score < 0.65:
        flag = "moderate"
    else:
        flag = "high"

    return {
        "risk_score": round(score, 2),
        "risk_flag": flag,
        "temperature_c": payload.temperature_c,
        "humidity_pct": payload.humidity_pct,
        "soil_moisture_pct": payload.soil_moisture_pct,
    }
