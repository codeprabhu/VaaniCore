# DSP specification

Target pipeline: DC-block (`y[n]=x[n]-x[n-1]+0.995*y[n-1]`) → pre-emphasis 0.97 → 512-sample Hann frames with 256-sample hop → 512-point real FFT → 40 mel bands from 20–4000 Hz → `log(x+1e-8)` → unnormalised DCT-II → 10 coefficients. Sample rate is 16 kHz. The Python reference is `ml/features.py`; the C reference is `firmware/components/dsp/mfcc.c`.

Current status: host-compiled C parity is verified with `make dsp-test`, max absolute error 0.01394 against the generated golden vector, below the 0.05 tolerance. This is a software test, not a hardware timing or accuracy measurement. No measured audio or model accuracy is present.
