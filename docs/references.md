# References and source ledger

These links support architecture, API, dataset, or component provenance only. They do not constitute VaaniCore
measurements, accuracy, power, pricing, lead-time, or hardware sign-off evidence.

## Embedded platform and protocol

- Espressif, ESP-IDF ESP32-S3 programming guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- Espressif, ESP32-S3 I2S API reference: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html
- Espressif, ESP32-S3 USB device stack: https://docs.espressif.com/projects/esp-idf/en/v6.0/esp32s3/api-reference/peripherals/usb_device.html
- Espressif Component Registry, `esp-tflite-micro`: https://components.espressif.com/components/espressif/esp-tflite-micro
- Espressif Component Registry, `esp-dsp`: https://components.espressif.com/components/espressif/esp-dsp
- TinyUSB documentation and CDC reference: https://docs.tinyusb.org/en/latest/ and https://docs.tinyusb.org/en/latest/reference/class/cdc.html
- TensorFlow Lite Micro source repository: https://github.com/tensorflow/tflite-micro

## Audio, datasets, and ML references

- InvenSense/TDK INMP441 datasheet: https://invensense.tdk.com/wp-content/uploads/2015/02/INMP441.pdf
- Warden, “Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition”: https://arxiv.org/abs/1804.03209
- Zhang et al., “Hello Edge: Keyword Spotting on Microcontrollers”: https://arxiv.org/abs/1711.07128
- Piczak, ESC-50 dataset repository and license notes: https://github.com/karolpiczak/ESC-50
- Vosk offline speech-recognition API: https://github.com/alphacep/vosk-api
- faster-whisper local transcription implementation: https://github.com/SYSTRAN/faster-whisper

## Electronics, simulation, and CAD

- Texas Instruments INA219 product and datasheet entry: https://www.ti.com/product/INA219/part-details/INA219AIDCNR
- ngspice documentation: https://ngspice.sourceforge.io/docs.html
- KiCad documentation: https://docs.kicad.org/
- CadQuery documentation: https://cadquery.readthedocs.io/en/stable/

## Items requiring human verification before final submission

- `[[HUMAN: verify exact ESP-IDF/component versions used in the firmware build]]`
- `[[HUMAN: verify dataset license compatibility and attribution for the intended distribution]]`
- `[[HUMAN: verify Indian vendor URLs, prices, stock, and lead times in hardware/bom.csv]]`
- `[[HUMAN: add any PETG/PLA/ABS material datasheet used for a mechanical claim]]`
- `[[HUMAN: add image attributions if any non-team visual is used; current intended images are team renders/photos]]`
