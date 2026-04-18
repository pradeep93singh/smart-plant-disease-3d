from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List, Optional
import os

from .schemas import ScanHistoryItem, SensorPayload

# Auto-detect DB from env or fallback sqlite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smart_plant.db")
engine = create_engine(DATABASE_URL, echo=True)

class ScanRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plant_name: str
    disease_name: str
    confidence_score: float
    severity_percentage: float
    urgency_level: str
    created_at: str = Field(default_factory=str)

class SensorRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    temperature: float
    humidity: float
    soil_moisture: float
    light_level: float

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def save_scan(plant_name: str, disease_name: str, confidence_score: float, severity_percentage: float, urgency_level: str):
    with Session(engine) as session:
        record = ScanRecord(
            plant_name=plant_name,
            disease_name=disease_name,
            confidence_score=confidence_score,
            severity_percentage=severity_percentage,
            urgency_level=urgency_level,
            created_at=str(datetime.now())
        )
        session.add(record)
        session.commit()

def list_scans(limit: int = 20):
    with Session(engine) as session:
        statement = select(ScanRecord).limit(limit)
        return session.exec(statement).all()

def update_sensor_state(payload: SensorPayload):
    with Session(engine) as session:
        record = SensorRecord(
            timestamp=payload.timestamp,
            temperature=payload.temperature,
            humidity=payload.humidity,
            soil_moisture=payload.soil_moisture,
            light_level=payload.light_level,
        )
        session.add(record)
        session.commit()
        return record

def get_latest_sensor_state():
    with Session(engine) as session:
        statement = select(SensorRecord).order_by(SensorRecord.timestamp.desc()).limit(1)
        result = session.exec(statement).first()
        return result
