"""Deterministic feature-pipeline smoke test; explicitly not an ML result."""
from __future__ import annotations
import argparse, json, pathlib
import numpy as np
from ml.features import mfcc

def main() -> int:
    p=argparse.ArgumentParser(description='Run a synthetic MFCC shape smoke test'); p.add_argument('--output', default='results/ml_smoke.json'); a=p.parse_args()
    x = np.zeros(16000, dtype=np.float32); features = mfcc(x)
    data = {'label': 'PIPELINE_SMOKE_TEST — NOT A RESULT', 'seed': 0, 'input': 'synthetic silence', 'feature_shape': list(features.shape), 'accuracy': None}
    out=pathlib.Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(data, indent=2) + '\n'); print(out)
if __name__ == '__main__': main()
