import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from passlib.context import CryptContext
from jose import jwt

from ..db import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, UserOut, TokenOut


router = APIRouter()

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = "HS256"
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "60"))


def _hash(pw: str) -> str:
    return pwd_ctx.hash(pw)


def _verify(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)


def _token_for_user(u: User) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(u.user_id),
        "username": u.username,
        "email": u.email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRE_MIN)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


@router.post("/register", response_model=UserOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    exists = db.scalar(
        select(User).where(
            or_(User.username == body.username, User.email == body.email)
        )
    )
    if exists:
        raise HTTPException(409, "Username or email already exists")
    u = User(
        username=body.username,
        email=body.email,
        password_hash=_hash(body.password),
        first_name=body.first_name,
        last_name=body.last_name,
        avatar_url=None,
        address=None,
        tel_no=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    if not body.username and not body.email:
        raise HTTPException(400, "Provide username or email")
    stmt = select(User)
    if body.username:
        stmt = stmt.where(User.username == body.username)
    else:
        stmt = stmt.where(User.email == body.email)
    u: Optional[User] = db.scalar(stmt)
    if not u or not _verify(body.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = _token_for_user(u)
    return TokenOut(access_token=token, user=u)
