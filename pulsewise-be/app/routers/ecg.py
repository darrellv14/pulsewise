from typing import List, Literal

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..ml.ecgnet import EXPECTED_LENGTH, predict_probs


router = APIRouter()


class ECGPredictIn(BaseModel):
    signal: List[float] = Field(
        ...,
        description="ECG signal values",
        min_length=EXPECTED_LENGTH,
        max_length=EXPECTED_LENGTH,
    )
    norm: Literal["zscore", "minmax", "none"] = "zscore"


class ECGPredictOut(BaseModel):
    probs: List[float]
    predicted_class: int


@router.post("/predict", response_model=ECGPredictOut)
def predict(body: ECGPredictIn):
    try:
        x = np.array(body.signal, dtype=np.float32)[None, :]
        if body.norm == "zscore":
            norm = "zscore"
        elif body.norm == "minmax":
            norm = "minmax"
        else:
            norm = "none"
        probs = predict_probs(x, norm=norm)
        pred = int(np.argmax(probs[0]))
        return ECGPredictOut(probs=probs[0].tolist(), predicted_class=pred)
    except ValueError as e:
        raise HTTPException(400, str(e))


class ECGPredictBatchIn(BaseModel):
    signals: List[List[float]] = Field(..., description="Batch of ECG signals")
    norm: Literal["zscore", "minmax", "none"] = "zscore"


class ECGPredictBatchOut(BaseModel):
    probs: List[List[float]]
    predicted_classes: List[int]


@router.post("/predict-batch", response_model=ECGPredictBatchOut)
def predict_batch(body: ECGPredictBatchIn):
    arr = np.array(body.signals, dtype=np.float32)
    if arr.ndim != 2 or arr.shape[1] != EXPECTED_LENGTH:
        raise HTTPException(
            400, f"Each signal must have length {EXPECTED_LENGTH}"
        )
    if body.norm == "zscore":
        norm = "zscore"
    elif body.norm == "minmax":
        norm = "minmax"
    else:
        norm = "none"
    probs = predict_probs(arr, norm=norm)
    preds = np.argmax(probs, axis=1).astype(int).tolist()
    return ECGPredictBatchOut(probs=probs.tolist(), predicted_classes=preds)
