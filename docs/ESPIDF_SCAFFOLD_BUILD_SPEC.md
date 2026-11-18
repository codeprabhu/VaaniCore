# ESP-IDF Scaffold and Build Specification

**Generated:** 2026-11-19T02:55:00Z
**Git Commit:** bc267ff
**Status:** APPROVED (scaffold complete, build BLOCKED on ESP-IDF install)

---

## Contract

**Scope:** ESP-IDF v5.x project structure for ESP32-S3 firmware build.

**Purpose:** Define complete scaffold ready for `idf.py build` once ESP-IDF installed.

---

## Project Structure

```
firmware/
├── CMakeLists.txt              # Root project, includes main + components
├── sdkconfig.defaults          # ESP32-S3 default configuration
├── main/
│   ├── CMakeLists.txt          # Main component sources
│   ├── main.c                  # app_main(), task creation
│   ├── pins.h                  # GPIO pin definitions
│   ├── intents.h/.c            # Intent classification table
│   ├── audio_capture.h/.c      # I2S/GDMA audio capture
│   ├── ui.h/.c                 # Buttons, LEDs, mute sense
├── components/
│   ├── protocol/
│   │   ├── CMakeLists.txt
│   │   ├── protocol.h/.c       # Frame encode/decode
│   │   ├── crc16.c             # CRC16-CCITT-FALSE
│   ├── dsp/
│   │   ├── CMakeLists.txt
│   │   ├── mfcc.h/.c           # MFCC feature extraction
│   ├── context/
│   │   ├── CMakeLists.txt
│   │   ├── context.h/.c        # 16-event history
│   │   ├── nvs_store.h/.c      # NVS persistence
```

---

## Root CMakeLists.txt (`firmware/CMakeLists.txt`)

```cmake
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(vaanicore)
```

- Minimal: just includes ESP-IDF project.cmake and sets project name
- Components auto-discovered in `components/` subdirectory

---

## Main Component (`firmware/main/CMakeLists.txt`)

```cmake
idf_component_register(
    SRCS "main.c" "audio_capture.c" "ui.c" "intents.c"
    INCLUDE_DIRS "."
    REQUIRES protocol dsp context
)
```

- Registers 4 source files
- Includes current directory for pins.h, intents.h
- Depends on 3 custom components

---

## Component CMakeLists.txt (each)

```cmake
# protocol/CMakeLists.txt
idf_component_register(
    SRCS "protocol.c" "crc16.c"
    INCLUDE_DIRS "."
)

# dsp/CMakeLists.txt
idf_component_register(
    SRCS "mfcc.c"
    INCLUDE_DIRS "."
)

# context/CMakeLists.txt
idf_component_register(
    SRCS "context.c" "nvs_store.c"
    INCLUDE_DIRS "."
)
```

---

## SDK Config Defaults (`firmware/sdkconfig.defaults`)

Key settings (abridged):
```ini
CONFIG_IDF_TARGET_ESP32S3=y
CONFIG_IDF_TARGET="esp32s3"
CONFIG_PARTITION_TABLE_CUSTOM=y
CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions.csv"
CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y
CONFIG_FREERTOS_HZ=1000
CONFIG_LOG_DEFAULT_LEVEL_INFO=y
CONFIG_TINYUSB_CDC_ENABLED=y
```

---

## FreeRTOS Task Architecture (`main.c`)

| Task | Priority | Core | Stack | Purpose |
|------|----------|------|-------|---------|
| audio_task | 6 | 0 | 4096 | I2S capture, ISR→task notify |
| dsp_task | 5 | 1 | 4096 | MFCC feature extraction (placeholder) |
| infer_task | 4 | 1 | 4096 | TFLite-Micro inference (placeholder) |
| intent_task | 3 | 1 | 3072 | Intent classification (placeholder) |
| context_task | 2 | 1 | 3072 | Context persistence (placeholder) |
| comms_task | 4 | 0 | 4096 | USB CDC protocol (placeholder) |
| ui_task | 2 | 1 | 3072 | Buttons, LEDs, mute |
| power_task | 1 | 1 | 3072 | Power management (placeholder) |

---

## Pin Assignments (`pins.h`)

| Signal | GPIO | Notes |
|--------|------|-------|
| I2S_BCLK | 4 | I2S clock |
| I2S_WS | 5 | I2S word select |
| I2S_DIN | 6 | I2S data in |
| I2C_SDA | 8 | I2C data (OLED) |
| I2C_SCL | 9 | I2C clock (OLED) |
| BUTTON_CONFIRM | 15 | Active low, pull-up |
| BUTTON_ABORT | 16 | Active low, pull-up |
| MUTE_SENSE | 17 | Privacy switch |
| LED_LISTEN | 18 | Status LED |
| LED_BUSY | 21 | Status LED |
| LED_ERR | 47 | Status LED |
| USB_DM | 19 | Native USB (reserved) |
| USB_DP | 20 | Native USB (reserved) |
| UART_TX | 43 | Debug UART |
| UART_RX | 44 | Debug UART |
| JTAG_TCK | 39 | JTAG |
| JTAG_TDO | 40 | JTAG |
| JTAG_TDI | 41 | JTAG |
| JTAG_TMS | 42 | JTAG |

---

## Build Commands

```bash
# One-time setup
export IDF_PATH=/path/to/esp-idf
. $IDF_PATH/export.sh

# In firmware/ directory
idf.py set-target esp32s3
idf.py build

# Flash (requires hardware)
idf.py -p /dev/ttyUSB0 flash monitor
```

---

## Current Status

| Component | Scaffold | Host-Tested | Hardware-Tested |
|-----------|----------|-------------|-----------------|
| Protocol | ✅ | ✅ (protocol-test) | ❌ |
| DSP (MFCC) | ✅ | ✅ (dsp-test) | ❌ |
| Context | ✅ | ✅ (context-test) | ❌ |
| Intents | ✅ | ✅ (intent-test) | ❌ |
| Audio Capture | ✅ (scaffold) | ❌ | ❌ |
| UI (Buttons/LEDs) | ✅ (scaffold) | ❌ | ❌ |
| NVS Store | ✅ | ❌ | ❌ |
| FreeRTOS Tasks | ✅ (created) | ❌ | ❌ |
| USB CDC | ✅ (TinyUSB config) | ❌ | ❌ |
| Full Build | ✅ (scaffold) | ❌ (no ESP-IDF) | ❌ |

---

## Invariants

1. **Component isolation** — Each component builds independently
2. **No heap in protocol/DSP/context** — Bounded buffers only
3. **Pin map single source** — `pins.h` validated against `hardware/pinmap.csv`
4. **Task priorities ordered** — Audio highest, power lowest
5. **Core affinity** — Audio/comms on core 0, others on core 1
6. **ESP32-S3 target** — sdkconfig.defaults sets target

---

## Acceptance Criteria

- Scaffold complete with all components
- CMakeLists.txt for root, main, and 3 components
- sdkconfig.defaults for ESP32-S3
- Pin assignments match hardware/pinmap.csv
- 8 tasks defined with priorities/cores
- Build BLOCKED on ESP-IDF install (human action)
- Next step (0294) can use this output