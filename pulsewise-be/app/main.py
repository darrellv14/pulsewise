from fastapi import FastAPI

app = FastAPI(title="PulseWise API")

@app.get("/health")
def health():
    return {"status": "ok"}
