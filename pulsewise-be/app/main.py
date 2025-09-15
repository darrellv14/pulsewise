import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import diaries, auth, meds, lifestyle, education
from .routers import ecg

app = FastAPI(title="PulseWise API")

# (opsional) tidak create_all karena database sudah ada via SQL init
# Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(diaries.router, prefix="/diaries", tags=["diaries"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(meds.router, prefix="/meds", tags=["medications"])
app.include_router(lifestyle.router, prefix="/lifestyle", tags=["lifestyle"])
app.include_router(education.router, prefix="/edu", tags=["education"])
app.include_router(ecg.router, prefix="/ecg", tags=["ecg"])

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:8080")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_origin,
        "http://localhost:3000",
        "http://pulsewise_frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
