# Firmware walkthrough

`firmware/main/main.c` creates named FreeRTOS tasks on the requested cores/priorities. `audio_capture.c` configures I2S standard mode with six DMA descriptors and posts a task notification from the receive callback; conversion happens in task context. `ui.c` routes GPIO events to a queue and controls three LEDs. `intents.c` provides a static 14-class lookup with risky/open-before-run flags. `context/nvs_store.c` persists the bounded event ring using NVS.

Viva questions: Why no copying in the ISR? To keep interrupt latency bounded. Why saturate samples? To avoid wraparound distortion. Why a bounded history? Predictable NVS/RAM use. Why a physical confirm? Speech recognition can be wrong. What is unverified? ESP-IDF compilation and board behavior.
