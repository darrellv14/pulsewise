import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import get_db
from ..models import DailyActivity, DailyConsumption, DiarySymptom


router = APIRouter()


@router.get("/activities", response_model=list[dict])
def list_activities(
    diary_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(DailyActivity).where(DailyActivity.diary_id == diary_id)
    ).all()
    return [
        {
            "activity_id": r.activity_id,
            "name": r.name,
            "duration_min": r.duration_min,
            "heart_rate": r.heart_rate,
            "user_feeling": r.user_feeling,
            "note": r.note,
            "occurred_at": r.occurred_at,
        }
        for r in rows
    ]


@router.post("/activities", response_model=dict)
def add_activity(
    diary_id: uuid.UUID,
    body: dict,
    db: Session = Depends(get_db),
):
    obj = DailyActivity(diary_id=diary_id, **body)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"activity_id": obj.activity_id}


@router.get("/consumptions", response_model=list[dict])
def list_consumptions(
    diary_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(DailyConsumption).where(DailyConsumption.diary_id == diary_id)
    ).all()
    return [
        {
            "consumption_id": r.consumption_id,
            "type": r.type,
            "name": r.name,
            "portion": r.portion,
            "sodium_mg": r.sodium_mg,
            "fluid_ml": r.fluid_ml,
            "note": r.note,
            "occurred_at": r.occurred_at,
        }
        for r in rows
    ]


@router.post("/consumptions", response_model=dict)
def add_consumption(
    diary_id: uuid.UUID,
    body: dict,
    db: Session = Depends(get_db),
):
    obj = DailyConsumption(diary_id=diary_id, **body)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"consumption_id": obj.consumption_id}


@router.get("/symptoms", response_model=list[dict])
def list_symptoms(
    diary_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(DiarySymptom).where(DiarySymptom.diary_id == diary_id)
    ).all()
    return [
        {
            "symptom_id": r.symptom_id,
            "type": r.type,
            "severity": r.severity,
            "note": r.note,
            "occurred_at": r.occurred_at,
        }
        for r in rows
    ]


@router.post("/symptoms", response_model=dict)
def add_symptom(
    diary_id: uuid.UUID,
    body: dict,
    db: Session = Depends(get_db),
):
    obj = DiarySymptom(diary_id=diary_id, **body)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"symptom_id": obj.symptom_id}
