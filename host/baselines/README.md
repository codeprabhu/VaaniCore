# P2/P3 baseline status

The host-ASR baselines are intentionally not installed in the bootstrap environment. `run_baseline.py` is the gated entry point. When a human supplies a model and audio conditions, implement P2 (device PCM stream + host ASR) and P3 (host microphone reference), logging CPU/RAM with `psutil`. Never put baseline numbers in the deck until they are produced by the benchmark scripts.
