from fastapi import FastAPI
from .routers import diaries
from .db import engine, Base

app = FastAPI(title="PulseWise API")

# (opsional) tidak create_all karena database sudah ada via SQL init
# Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(diaries.router, prefix="/diaries", tags=["diaries"])
