from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from datetime import datetime, date, time
from sqlalchemy import (Integer, 
    Date,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    TIMESTAMP,
    Time,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    avatar_url: Mapped[str | None]
    address: Mapped[str | None]
    tel_no: Mapped[str | None]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]


class HeartDiary(Base):
    __tablename__ = "heart_diaries"
    diary_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID]
    diary_date: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )

    vitals: Mapped[list["VitalSign"]] = relationship(
        "VitalSign", back_populates="diary", cascade="all,delete"
    )


class VitalSign(Base):
    __tablename__ = "vital_signs"
    vital_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    diary_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("heart_diaries.diary_id", ondelete="CASCADE")
    )
    measured_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    height_cm: Mapped[float | None] = mapped_column(Numeric(5, 1))
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5, 2))
    bmi: Mapped[float | None] = mapped_column(Numeric(4, 1))
    systolic: Mapped[int | None] = mapped_column(Integer)
    diastolic: Mapped[int | None] = mapped_column(Integer)
    heart_rate: Mapped[int | None] = mapped_column(Integer)
    oxygen_saturation: Mapped[int | None] = mapped_column(Integer)
    body_temp_c: Mapped[float | None] = mapped_column(Numeric(4, 2))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )

    diary: Mapped[HeartDiary] = relationship(
        "HeartDiary", back_populates="vitals"
    )


class Medication(Base):
    __tablename__ = "medications"
    medication_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID]
    name: Mapped[str]
    description: Mapped[str | None]
    condition_tag: Mapped[str | None]
    dosage_amount: Mapped[float | None] = mapped_column(Numeric(10, 3))
    dosage_unit: Mapped[str | None]
    route: Mapped[str | None]
    active: Mapped[bool]
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    schedule_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medications.medication_id", ondelete="CASCADE")
    )
    time_of_day: Mapped[time | None] = mapped_column(Time)
    days_of_week: Mapped[list[int] | None] = mapped_column(ARRAY(Integer), nullable=True)
    timezone: Mapped[str]
    as_needed: Mapped[bool]
    interval_days: Mapped[int]
    remind_offset_min: Mapped[int | None]
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class MedicationLog(Base):
    __tablename__ = "medication_logs"
    medication_log_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medications.medication_id", ondelete="CASCADE")
    )
    schedule_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("medication_schedules.schedule_id", ondelete="SET NULL")
    )
    planned_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    taken_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    taken: Mapped[bool]
    notes: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class DailyConsumption(Base):
    __tablename__ = "daily_consumptions"
    consumption_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    diary_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("heart_diaries.diary_id", ondelete="CASCADE")
    )
    type: Mapped[str]
    name: Mapped[str]
    portion: Mapped[str | None]
    sodium_mg: Mapped[int | None]
    fluid_ml: Mapped[int | None]
    note: Mapped[str | None]
    occurred_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class DailyActivity(Base):
    __tablename__ = "daily_activities"
    activity_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    diary_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("heart_diaries.diary_id", ondelete="CASCADE")
    )
    name: Mapped[str]
    duration_min: Mapped[int]
    heart_rate: Mapped[int | None]
    user_feeling: Mapped[str | None]
    note: Mapped[str | None]
    occurred_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class DiarySymptom(Base):
    __tablename__ = "diary_symptoms"
    symptom_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    diary_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("heart_diaries.diary_id", ondelete="CASCADE")
    )
    type: Mapped[str]
    severity: Mapped[int]
    note: Mapped[str | None]
    occurred_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class EducationModule(Base):
    __tablename__ = "education_modules"
    module_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    slug: Mapped[str]
    title: Mapped[str]
    description: Mapped[str | None]
    cover_url: Mapped[str | None]
    language: Mapped[str | None]
    is_published: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class EducationSection(Base):
    __tablename__ = "education_sections"
    section_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    module_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("education_modules.module_id", ondelete="CASCADE")
    )
    title: Mapped[str]
    body_md: Mapped[str | None]
    order: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow
    )


class EducationProgress(Base):
    __tablename__ = "education_progress"
    progress_id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID]
    module_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("education_modules.module_id", ondelete="CASCADE")
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True)
    )
