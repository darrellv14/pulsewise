import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..db import get_db
from ..models import EducationModule, EducationSection, EducationProgress


router = APIRouter()


@router.get("/modules", response_model=list[dict])
def list_modules(db: Session = Depends(get_db)):
    rows = db.scalars(
        select(EducationModule).where(
            EducationModule.is_published == True  # noqa: E712
        )
    ).all()
    return [
        {
            "module_id": r.module_id,
            "slug": r.slug,
            "title": r.title,
            "description": r.description,
            "cover_url": r.cover_url,
            "language": r.language,
        }
        for r in rows
    ]


@router.get("/modules/{module_id}/sections", response_model=list[dict])
def list_sections(module_id: uuid.UUID, db: Session = Depends(get_db)):
    rows = db.scalars(
        select(EducationSection)
        .where(EducationSection.module_id == module_id)
        .order_by(EducationSection.order.asc())
    ).all()
    return [
        {
            "section_id": r.section_id,
            "title": r.title,
            "body_md": r.body_md,
            "order": r.order,
        }
        for r in rows
    ]


@router.get("/progress", response_model=list[dict])
def list_progress(user_id: uuid.UUID, db: Session = Depends(get_db)):
    rows = db.scalars(
        select(EducationProgress).where(EducationProgress.user_id == user_id)
    ).all()
    return [
        {
            "progress_id": r.progress_id,
            "module_id": r.module_id,
            "completed_at": r.completed_at,
        }
        for r in rows
    ]


@router.post("/progress/{module_id}", response_model=dict)
def mark_completed(
    user_id: uuid.UUID,
    module_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    ex = db.scalar(
        select(EducationProgress)
        .where(EducationProgress.user_id == user_id)
        .where(EducationProgress.module_id == module_id)
    )
    now = datetime.utcnow()
    if ex:
        ex.completed_at = now
        db.commit()
        db.refresh(ex)
        return {
            "progress_id": ex.progress_id,
            "completed_at": ex.completed_at,
        }
    obj = EducationProgress(
        user_id=user_id,
        module_id=module_id,
        completed_at=now,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {
        "progress_id": obj.progress_id,
        "completed_at": obj.completed_at,
    }
