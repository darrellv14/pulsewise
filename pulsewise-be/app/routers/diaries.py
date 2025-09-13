import uuid
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from ..db import get_db
from ..models import HeartDiary, VitalSign
from ..schemas import DiaryCreate, DiaryUpdate, DiaryOut, VitalCreate, VitalOut

router = APIRouter()

# ---- Diaries
@router.post("", response_model=DiaryOut)
def create_diary(body: DiaryCreate, db: Session = Depends(get_db)):
    # enforce unique (user_id, diary_date)
    exists = db.scalar(select(HeartDiary).where(and_(
        HeartDiary.user_id==body.user_id,
        HeartDiary.diary_date==body.diary_date
    )))
    if exists:
        raise HTTPException(409, "Diary for this user & date already exists")
    d = HeartDiary(**body.model_dump())
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.get("", response_model=list[DiaryOut])
def list_diaries(
    user_id: uuid.UUID,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    stmt = select(HeartDiary).where(HeartDiary.user_id==user_id)
    if date_from:
        stmt = stmt.where(HeartDiary.diary_date >= date_from)
    if date_to:
        stmt = stmt.where(HeartDiary.diary_date <= date_to)
    stmt = stmt.order_by(HeartDiary.diary_date.desc()).limit(limit)
    rows = db.scalars(stmt).all()
    return rows

@router.get("/{diary_id}", response_model=DiaryOut)
def get_diary(diary_id: uuid.UUID, db: Session = Depends(get_db)):
    d = db.get(HeartDiary, diary_id)
    if not d:
        raise HTTPException(404, "Diary not found")
    return d

@router.put("/{diary_id}", response_model=DiaryOut)
def update_diary(diary_id: uuid.UUID, body: DiaryUpdate, db: Session = Depends(get_db)):
    d = db.get(HeartDiary, diary_id)
    if not d:
        raise HTTPException(404, "Diary not found")
    if body.notes is not None:
        d.notes = body.notes
    db.commit(); db.refresh(d)
    return d

@router.delete("/{diary_id}")
def delete_diary(diary_id: uuid.UUID, db: Session = Depends(get_db)):
    d = db.get(HeartDiary, diary_id)
    if not d:
        raise HTTPException(404, "Diary not found")
    db.delete(d); db.commit()
    return {"ok": True}

# ---- Vitals (nested)
@router.post("/{diary_id}/vitals", response_model=VitalOut)
def add_vital(diary_id: uuid.UUID, body: VitalCreate, db: Session = Depends(get_db)):
    if not db.get(HeartDiary, diary_id):
        raise HTTPException(404, "Diary not found")
    v = VitalSign(diary_id=diary_id, **body.model_dump())
    db.add(v); db.commit(); db.refresh(v)
    return v

@router.get("/{diary_id}/vitals", response_model=list[VitalOut])
def list_vitals(diary_id: uuid.UUID, db: Session = Depends(get_db)):
    if not db.get(HeartDiary, diary_id):
        raise HTTPException(404, "Diary not found")
    rows = db.query(VitalSign).filter(VitalSign.diary_id==diary_id).order_by(VitalSign.measured_at.desc()).all()
    return rows
