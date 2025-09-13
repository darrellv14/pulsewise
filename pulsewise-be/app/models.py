import uuid
from datetime import datetime, date
from sqlalchemy import Date, ForeignKey, Integer, Numeric, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class HeartDiary(Base):
    __tablename__ = "heart_diaries"
    diary_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID]
    diary_date: Mapped[date] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    vitals: Mapped[list["VitalSign"]] = relationship("VitalSign", back_populates="diary", cascade="all,delete")

class VitalSign(Base):
    __tablename__ = "vital_signs"
    vital_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    diary_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("heart_diaries.diary_id", ondelete="CASCADE"))
    measured_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    height_cm: Mapped[float | None] = mapped_column(Numeric(5,1))
    weight_kg: Mapped[float | None] = mapped_column(Numeric(5,2))
    bmi: Mapped[float | None] = mapped_column(Numeric(4,1))
    systolic: Mapped[int | None] = mapped_column(Integer)
    diastolic: Mapped[int | None] = mapped_column(Integer)
    heart_rate: Mapped[int | None] = mapped_column(Integer)
    oxygen_saturation: Mapped[int | None] = mapped_column(Integer)
    body_temp_c: Mapped[float | None] = mapped_column(Numeric(4,2))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    diary: Mapped[HeartDiary] = relationship("HeartDiary", back_populates="vitals")
