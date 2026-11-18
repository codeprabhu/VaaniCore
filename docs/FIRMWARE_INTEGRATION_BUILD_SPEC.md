# Firmware Integration and Build Specification

**Generated:** 2026-11-19T03:45:00Z
**Git Commit:** bc267ff
**Status:** APPROVED (scaffold complete, build BLOCKED on ESP-IDF)

---

## Contract

**Scope:** Complete ESP32-S3 firmware integration with all components, FreeRTOS tasks, and build configuration.

**Purpose:** Define integrated firmware ready for ESP-IDF build.

---

## Task Architecture (`main.c`)

| Task | Function | Priority | Core | Stack | Queue Connections |
|------|----------|----------|------|-------|-------------------|
| audio_task | vaanicore_audio_task | 6 | 0 | 4096 | → dsp_queue |
| dsp_task | vaanicore_dsp_task | 5 | 1 | 4096 | audio_queue → infer_queue |
| infer_task | vaanicore_infer_task | 4 | 1 | 4096 | dsp_queue → intent_queue |
| intent_task | vaanicore_intent_task | 3 | 1 | 3072 | infer_queue → comms_tx_queue |
| context_task | vaanicore_context_task | 2 | 1 | 3072 | PROJECT_EVENT → NVS |
| comms_task | vaanicore_comms_task | 4 | 0 | 4096 | comms_tx_queue → USB CDC |
| ui_task | vaanicore_ui_task | 2 | 1 | 3072 | ui_events_queue → intent/comms |
| power_task | vaanicore_power_task | 1 | 1 | 3072 | — |

---

## Queue Definitions

```c
// main.c
QueueHandle_t audio_queue;      // int16_t[256] frames
QueueHandle_t dsp_queue;        // float[10] MFCC frames
QueueHandle_t infer_queue;      // Classifier output (class_name)
QueueHandle_t intent_queue;     // vc_intent_t*
QueueHandle_t comms_tx_queue;   // Encoded frames (char[128])
QueueHandle_t ui_events_queue;  // vc_ui_event_t
```

---

## Component Integration

| Component | Used By | Functions |
|-----------|---------|-----------|
| protocol | comms_task, intent_task | vaanicore_encode_frame, vaanicore_decode_frame |
| dsp | dsp_task | mfcc_init, mfcc_process |
| context | context_task, intent_task | vc_history_init, vc_history_append, vc_history_resolve_confirmed, vc_nvs_init, vc_nvs_save |

---

## Data Flow

```
Microphone
    ↓ I2S/GDMA (audio_task)
int16_t[256] frames
    ↓ audio_queue
MFCC (dsp_task) → float[10]
    ↓ dsp_queue
Classifier (infer_task) → class_name
    ↓ infer_queue
Intent lookup (intent_task) → vc_intent_t → frame encode
    ↓ comms_tx_queue
USB CDC (comms_task) → Host
    ↓
Host response → comms_task → decode → session update
    ↓
PROJECT_EVENT → context_task → vc_history_append → NVS
```

---

## Build Configuration

### `firmware/CMakeLists.txt`
```cmake
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(vaanicore)
```

### `firmware/main/CMakeLists.txt`
```cmake
idf_component_register(
    SRCS "main.c" "audio_capture.c" "ui.c" "intents.c"
    INCLUDE_DIRS "."
    REQUIRES protocol dsp context
)
```

### Component CMakeLists.txt
Each component registers its sources and includes.

---

## SDK Config (`sdkconfig.defaults`)

Key settings:
- `CONFIG_IDF_TARGET_ESP32S3=y`
- `CONFIG_PARTITION_TABLE_CUSTOM=y`
- `CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y`
- `CONFIG_FREERTOS_HZ=1000`
- `CONFIG_TINYUSB_CDC_ENABLED=y`
- `CONFIG_LOG_DEFAULT_LEVEL_INFO=y`

---

## Build Commands

```bash
# Setup (one-time)
export IDF_PATH=/path/to/esp-idf-v5.x
. $IDF_PATH/export.sh

# Build
cd firmware
idf.py set-target esp32s3
idf.py build

# Output
# build/bootloader/bootloader.bin
# build/partition_table/partition-table.bin
# build/vaanicore.bin

# Flash (requires hardware)
idf.py -p /dev/ttyUSB0 flash monitor
```

---

## Current Status

| Item | Status |
|------|--------|
| Scaffold | ✅ Complete |
| Component C code | ✅ Complete |
| CMakeLists.txt | ✅ Complete |
| sdkconfig.defaults | ✅ Complete |
| Pin validation | ✅ Pass |
| Host C tests | ✅ Pass (protocol, context, DSP, intents) |
| ESP-IDF build | ❌ BLOCKED (no ESP-IDF) |
| Hardware flash/test | ❌ BLOCKED (no hardware) |

---

## Invariants

1. **Task priorities ordered** — Audio(6) > DSP(5) > Infer(4)=Comms(4) > Intent(3) > Context(2) > UI(2) > Power(1)
2. **Core affinity** — Audio/Comms on core 0; others on core 1
3. **Queue boundaries** — Fixed sizes, no dynamic allocation
4. **Component isolation** — Each builds independently via CMake
5. **Pin validation** — pins.h matches hardware/pinmap.csv
6. **No heap in hot path** — Protocol, DSP, context use stack/static
7. **Deterministic build** — sdkconfig.defaults pins versions
8. **OTA ready** — Partition table supports factory + ota_0 + ota_1

---

## Acceptance Criteria

- 8 tasks defined with priorities, cores, stacks, queues
- Data flow documented end-to-end
- Component integration specified
- Build commands documented
- 8 invariants enumerated
- Build BLOCKED on ESP-IDF install (human action)
- Next step (0344) can use this output