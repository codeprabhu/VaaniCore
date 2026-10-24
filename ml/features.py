"""Reference MFCC shape and deterministic feature stub; hardware parity spec is in docs/dsp_spec.md."""
from __future__ import annotations
import argparse, numpy as np

def mfcc(samples: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
    samples = np.asarray(samples, dtype=np.float32)
    frames = max(1, 1 + (len(samples) - 512) // 256)
    out = np.zeros((frames, 10), dtype=np.float32)
    for i in range(frames):
        frame = samples[i * 256:i * 256 + 512]
        frame = np.pad(frame, (0, max(0, 512 - len(frame))))[:512]
        out[i, 0] = float(np.log(np.mean(frame * frame) + 1e-8))
    return out

def main():
    p = argparse.ArgumentParser(); p.add_argument("--help-only", action="store_true"); p.parse_args()
    print("feature reference ready; no dataset result generated")
if __name__ == "__main__": main()
