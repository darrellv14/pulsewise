import os
from typing import Optional

import numpy as np
import torch
from torch import nn


class Conv2dWithConstraint(nn.Conv2d):
    def __init__(self, *args, max_norm: float = 1.0, **kwargs):
        self.max_norm = max_norm
        super().__init__(*args, **kwargs)

    def forward(self, x):  # type: ignore[override]
        self.weight.data = torch.renorm(
            self.weight.data, p=2, dim=0, maxnorm=self.max_norm
        )
        return super().forward(x)


class ECGNet(nn.Module):
    def InitialBlocks(self, dropoutRate: float):
        block1 = nn.Sequential(
            nn.Conv2d(
                1,
                self.F1,
                (1, self.kernelLength),
                stride=1,
                padding=(0, self.kernelLength // 2),
                bias=False,
            ),
            nn.BatchNorm2d(self.F1, momentum=0.01, affine=True, eps=1e-3),
            Conv2dWithConstraint(
                self.F1,
                self.F1 * self.D,
                (self.channels, 1),
                max_norm=1,
                stride=1,
                padding=(0, 0),
                groups=self.F1,
                bias=False,
            ),
            nn.BatchNorm2d(
                self.F1 * self.D, momentum=0.01, affine=True, eps=1e-3
            ),
            nn.ELU(),
            nn.AvgPool2d((1, 4), stride=4),
            nn.Dropout(p=dropoutRate),
        )
        block2 = nn.Sequential(
            nn.Conv2d(
                self.F1 * self.D,
                self.F1 * self.D,
                (1, self.kernelLength2),
                stride=1,
                padding=(0, self.kernelLength2 // 2),
                bias=False,
                groups=self.F1 * self.D,
            ),
            nn.Conv2d(
                self.F1 * self.D,
                self.F2,
                1,
                padding=(0, 0),
                groups=1,
                bias=False,
                stride=1,
            ),
            nn.BatchNorm2d(self.F2, momentum=0.01, affine=True, eps=1e-3),
            nn.ELU(),
            nn.AvgPool2d((1, 8), stride=8),
            nn.Dropout(p=dropoutRate),
        )
        return nn.Sequential(block1, block2)

    def ClassifierBlock(self, inputSize: int, n_classes: int):
        return nn.Sequential(
            nn.Linear(inputSize, n_classes, bias=False),
            nn.Softmax(dim=1),
        )

    def CalculateOutSize(self, model: nn.Module, channels: int, samples: int):
        data = torch.rand(1, 1, channels, samples)
        model.eval()
        out = model(data).shape
        return out[2:]

    def __init__(
        self,
        n_classes: int = 2,
        channels: int = 1,
        samples: int = 187,
        dropoutRate: float = 0.0,
        kernelLength: int = 64,
        kernelLength2: int = 16,
        F1: int = 8,
        D: int = 2,
        F2: int = 16,
    ):
        super().__init__()
        self.F1 = F1
        self.F2 = F2
        self.D = D
        self.samples = samples
        self.n_classes = n_classes
        self.channels = channels
        self.kernelLength = kernelLength
        self.kernelLength2 = kernelLength2
        self.dropoutRate = dropoutRate

        self.blocks = self.InitialBlocks(dropoutRate)
        self.blockOutputSize = self.CalculateOutSize(
            self.blocks, channels, samples
        )
        self.classifierBlock = self.ClassifierBlock(
            self.F2 * self.blockOutputSize[1], n_classes
        )

    def forward(self, x):  # type: ignore[override]
        x = self.blocks(x)
        x = x.view(x.size(0), -1)
        x = self.classifierBlock(x)
        return x


EXPECTED_LENGTH = int(os.getenv("ECG_SIGNAL_LENGTH", "187"))
WEIGHTS_PATH = os.getenv("ECG_WEIGHTS_PATH", "")

_MODEL: Optional[ECGNet] = None


def _build_model() -> ECGNet:
    model = ECGNet(
        n_classes=2,
        channels=1,
        samples=EXPECTED_LENGTH,
        dropoutRate=0.0,
        kernelLength=64,
        kernelLength2=16,
        F1=8,
        D=2,
        F2=16,
    )
    return model


def get_model() -> ECGNet:
    global _MODEL
    if _MODEL is None:
        model = _build_model()
        if WEIGHTS_PATH and os.path.isfile(WEIGHTS_PATH):
            state = torch.load(WEIGHTS_PATH, map_location="cpu")
            # Accept either full state_dict or model.state_dict() keys
            if isinstance(state, dict) and all(
                k.startswith("blocks") or k.startswith("classifierBlock")
                for k in state.keys()
            ):
                model.load_state_dict(state)  # type: ignore[arg-type]
            elif (
                isinstance(state, dict)
                and "state_dict" in state
                and isinstance(state["state_dict"], dict)
            ):
                model.load_state_dict(
                    state["state_dict"]
                )  # type: ignore[arg-type]
            else:
                # try strict=False to be tolerant
                model.load_state_dict(
                    state, strict=False
                )  # type: ignore[arg-type]
        _MODEL = model.eval()
    return _MODEL


def normalize_signal(x: np.ndarray, method: str = "zscore") -> np.ndarray:
    if method == "zscore":
        mean = x.mean()
        std = x.std()
        if std < 1e-8:
            std = 1.0
        return (x - mean) / std
    if method == "minmax":
        mn = x.min()
        mx = x.max()
        if abs(mx - mn) < 1e-8:
            return np.zeros_like(x)
        return (x - mn) / (mx - mn)
    return x


def predict_probs(signals: np.ndarray, norm: str = "zscore") -> np.ndarray:
    if signals.ndim != 2:
        raise ValueError("signals must be 2D: (batch, length)")
    if signals.shape[1] != EXPECTED_LENGTH:
        raise ValueError(f"Each signal must have length {EXPECTED_LENGTH}")

    # Normalize per sample
    signals = np.stack([normalize_signal(s, norm) for s in signals], axis=0)

    model = get_model()
    with torch.no_grad():
        t = torch.from_numpy(signals.astype(np.float32))  # (N, L)
        # (N, 1, L) then (N, 1, 1, L)
        t = t.unsqueeze(1)
        t = t.unsqueeze(1)  # (N, 1, 1, L)
        out = model(t)
        probs = out.cpu().numpy()
        return probs
