import uuid
from datetime import date, datetime
from pydantic import BaseModel, Field, conint, ConfigDict

# ---- Diaries
class DiaryBase(BaseModel):
    user_id: uuid.UUID
    diary_date: date
    notes: str | None = None

class DiaryCreate(DiaryBase):
    pass

class DiaryUpdate(BaseModel):
    notes: str | None = None

class DiaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    diary_id: uuid.UUID
    user_id: uuid.UUID
    diary_date: date
    notes: str | None = None

# ---- Vitals
class VitalCreate(BaseModel):
    measured_at: datetime
    height_cm: float | None = None
    weight_kg: float | None = None
    bmi: float | None = None
    systolic: conint(ge=50, le=260) | None = None
    diastolic: conint(ge=30, le=200) | None = None
    heart_rate: conint(ge=20, le=250) | None = None
    oxygen_saturation: conint(ge=30, le=100) | None = None
    body_temp_c: float | None = None

class VitalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    vital_id: uuid.UUID
    diary_id: uuid.UUID
    measured_at: datetime
    height_cm: float | None
    weight_kg: float | None
    bmi: float | None
    systolic: int | None
    diastolic: int | None
    heart_rate: int | None
    oxygen_saturation: int | None
    body_temp_c: float | None
