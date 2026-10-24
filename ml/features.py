"""Reference MFCC implementation shared by training and the firmware parity test."""
from __future__ import annotations
import argparse
import numpy as np

SAMPLE_RATE = 16000
FRAME = 512
HOP = 256
MELS = 40
COEFFS = 10
EPS = 1e-8

def _mel(hz: np.ndarray) -> np.ndarray:
    return 2595.0 * np.log10(1.0 + hz / 700.0)

def _hz(mel: np.ndarray) -> np.ndarray:
    return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)

def melbank(sample_rate: int = SAMPLE_RATE, nfft: int = FRAME, bands: int = MELS) -> np.ndarray:
    low, high = _mel(np.array([20.0, min(4000.0, sample_rate / 2)]))
    points = _hz(np.linspace(low, high, bands + 2))
    bins = np.floor((nfft + 1) * points / sample_rate).astype(int)
    bank = np.zeros((bands, nfft // 2 + 1), dtype=np.float32)
    for m in range(1, bands + 1):
        left, center, right = int(bins[m - 1]), int(bins[m]), int(bins[m + 1])
        if center <= left: center = left + 1
        if right <= center: right = center + 1
        for k in range(max(0, left), min(center, bank.shape[1])):
            bank[m - 1, k] = (k - left) / (center - left)
        for k in range(max(0, center), min(right, bank.shape[1])):
            bank[m - 1, k] = (right - k) / (right - center)
    return bank

def mfcc_frame(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Return ten unnormalised DCT-II coefficients for one 512-sample frame."""
    x = np.asarray(samples, dtype=np.float32).reshape(-1)
    x = np.pad(x, (0, max(0, FRAME - len(x))))[:FRAME]
    hp = np.empty(FRAME, dtype=np.float32)
    previous = 0.0
    hp_previous = 0.0
    for i, sample in enumerate(x):
        hp[i] = sample - previous + 0.995 * hp_previous
        previous, hp_previous = float(sample), float(hp[i])
    emphasized = np.empty(FRAME, dtype=np.float32)
    emphasized[0] = hp[0]
    emphasized[1:] = hp[1:] - 0.97 * hp[:-1]
    windowed = emphasized * np.hanning(FRAME).astype(np.float32)
    spectrum = np.abs(np.fft.rfft(windowed, n=FRAME)).astype(np.float32) ** 2
    energies = melbank(sample_rate) @ spectrum
    log_energies = np.log(energies + EPS)
    indices = np.arange(MELS, dtype=np.float32)
    return np.asarray([np.sum(log_energies * np.cos(np.pi * k * (2.0 * indices + 1.0) / (2.0 * MELS))) for k in range(COEFFS)], dtype=np.float32)

def mfcc(samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    samples = np.asarray(samples, dtype=np.float32).reshape(-1)
    frames = max(1, 1 + max(0, len(samples) - FRAME) // HOP)
    return np.vstack([mfcc_frame(samples[i * HOP:i * HOP + FRAME], sample_rate) for i in range(frames)])

def main() -> None:
    parser = argparse.ArgumentParser(description="Compute VaaniCore reference MFCCs")
    parser.add_argument("--samples", type=int, default=16000)
    args = parser.parse_args()
    print({"frames": mfcc(np.zeros(args.samples, dtype=np.float32)).shape[0], "coefficients": COEFFS, "label": "REFERENCE_PIPELINE"})

if __name__ == "__main__":
    main()
