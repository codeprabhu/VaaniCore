# DSP specification

Target pipeline: DC-block → pre-emphasis 0.97 → 512-sample Hann frames with 256-sample hop → 512-point real FFT → 40 mel bands from 20–4000 Hz → `log(x+1e-8)` → DCT-II → 10 coefficients. Sample rate is 16 kHz. The Python reference is `ml/features.py`; the production implementation and golden-vector parity test remain `[[HUMAN: run after ESP-IDF/C toolchain is installed]]`.

Current status: `TARGET` specification only. No measured audio or model accuracy is present.
