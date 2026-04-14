from datetime import datetime
from typing import List

from sqlmodel import Field, Session, SQLModel, create_engine, select


class ScanRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plant_name: str
    disease_name: str
    confidence_score: float
    severity_percentage: float
    urgency_level: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


engine = create_engine("sqlite:///smart_plant.db")


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def save_scan(
    plant_name: str,
    disease_name: str,
    confidence_score: float,
    severity_percentage: float,
    urgency_level: str,
) -> ScanRecord:
    record = ScanRecord(
        plant_name=plant_name,
        disease_name=disease_name,
        confidence_score=confidence_score,
        severity_percentage=severity_percentage,
        urgency_level=urgency_level,
    )
    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
    return record


def list_scans(limit: int = 50) -> List[ScanRecord]:
    with Session(engine) as session:
        statement = select(ScanRecord).order_by(ScanRecord.created_at.desc()).limit(limit)
        return list(session.exec(statement))
