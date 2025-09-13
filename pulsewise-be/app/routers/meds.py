import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import get_db
from ..models import Medication, MedicationSchedule, MedicationLog


router = APIRouter()


@router.get("", response_model=list[dict])
def list_meds(user_id: uuid.UUID, db: Session = Depends(get_db)):
    rows = db.scalars(
        select(Medication).where(Medication.user_id == user_id)
    ).all()
    return [
        {
            "medication_id": r.medication_id,
            "user_id": r.user_id,
            "name": r.name,
            "description": r.description,
            "condition_tag": r.condition_tag,
            "dosage_amount": (
                float(r.dosage_amount) if r.dosage_amount is not None else None
            ),
            "dosage_unit": r.dosage_unit,
            "route": r.route,
            "active": r.active,
            "start_date": r.start_date,
            "end_date": r.end_date,
        }
        for r in rows
    ]


@router.post("", response_model=dict)
def create_med(body: dict, db: Session = Depends(get_db)):
    m = Medication(**body)
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"medication_id": m.medication_id}


@router.get("/{medication_id}/schedules", response_model=list[dict])
def list_schedules(medication_id: uuid.UUID, db: Session = Depends(get_db)):
    rows = db.scalars(
        select(MedicationSchedule).where(
            MedicationSchedule.medication_id == medication_id
        )
    ).all()
    return [
        {
            "schedule_id": r.schedule_id,
            "time_of_day": r.time_of_day,
            "days_of_week": r.days_of_week,
            "timezone": r.timezone,
            "as_needed": r.as_needed,
            "interval_days": r.interval_days,
            "remind_offset_min": r.remind_offset_min,
            "start_date": r.start_date,
            "end_date": r.end_date,
        }
        for r in rows
    ]


@router.post("/{medication_id}/schedules", response_model=dict)
def create_schedule(
    medication_id: uuid.UUID, body: dict, db: Session = Depends(get_db)
):
    sc = MedicationSchedule(medication_id=medication_id, **body)
    db.add(sc)
    db.commit()
    db.refresh(sc)
    return {"schedule_id": sc.schedule_id}


@router.get("/{medication_id}/logs", response_model=list[dict])
def list_logs(
    medication_id: uuid.UUID,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(MedicationLog)
        .where(MedicationLog.medication_id == medication_id)
        .order_by(MedicationLog.taken_at.desc())
        .limit(limit)
    ).all()
    return [
        {
            "medication_log_id": r.medication_log_id,
            "schedule_id": r.schedule_id,
            "planned_at": r.planned_at,
            "taken_at": r.taken_at,
            "taken": r.taken,
            "notes": r.notes,
        }
        for r in rows
    ]


@router.post("/{medication_id}/logs", response_model=dict)
def create_log(
    medication_id: uuid.UUID, body: dict, db: Session = Depends(get_db)
):
    lg = MedicationLog(
        medication_id=medication_id, **body
    )
    db.add(lg)
    db.commit()
    db.refresh(lg)
    return {"medication_log_id": lg.medication_log_id}
