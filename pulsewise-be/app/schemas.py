import uuid
from datetime import date, datetime
from typing import Annotated
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
    systolic: Annotated[int, conint(ge=50, le=260)] | None = None
    diastolic: Annotated[int, conint(ge=30, le=200)] | None = None
    heart_rate: Annotated[int, conint(ge=20, le=250)] | None = None
    oxygen_saturation: Annotated[int, conint(ge=30, le=100)] | None = None
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


# ---- Auth / Users


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str | None = None
    avatar_url: str | None = None
    address: str | None = None
    tel_no: str | None = None


class RegisterIn(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=6)
    first_name: str
    last_name: str | None = None


class LoginIn(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
