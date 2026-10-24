# DSP walkthrough

`ml/features.py` is the numerical reference: DC-block, pre-emphasis, Hann, real FFT, mel bank, log, and DCT-II. `firmware/components/dsp/mfcc.c` mirrors one frame with a simple DFT for parity testing; production firmware can replace that DFT with ESP-DSP while retaining the vector contract. `make dsp-test` compiles the C test and checks max error below 0.05.

Viva questions: Why 512 samples? It gives a 32 ms frame at 16 kHz. Why 256 hop? It gives 16 ms update spacing. Why mel bands? They compress frequency resolution perceptually. Why compare golden vectors? Python/C drift is a common embedded ML failure. What is not measured yet? ESP-DSP timing on ESP32-S3.
