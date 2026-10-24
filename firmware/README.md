# ESP-IDF firmware status

The ESP-IDF target skeleton includes FreeRTOS tasks, I2S standard-mode GDMA configuration (6 descriptors × 256 frames), ISR-to-task notification, 32-bit-to-16-bit saturation, protocol/DSP/context components, and an NVS adapter for the 16-event history. A complete build is not claimed because ESP-IDF and the official component versions are not installed in this environment. Human command after installation: `idf.py set-target esp32s3 && idf.py build`.
