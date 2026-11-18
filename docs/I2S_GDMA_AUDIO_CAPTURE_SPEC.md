# I2S/GDMA Audio Capture Specification

**Generated:** 2026-11-19T03:05:00Z
**Git Commit:** bc267ff
**Status:** APPROVED (scaffold complete, hardware validation BLOCKED)

---

## Contract

**Scope:** ESP32-S3 I2S standard mode with GDMA for 16kHz mono audio capture.

**Purpose:** Define audio capture pipeline ready for hardware validation.

---

## Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Sample Rate | 16 kHz | DSP spec |
| Channels | 1 (mono) | I2S_DIN only |
| Bit Depth | 32-bit I2S → 16-bit saturated | audio_capture.c |
| Frame Size | 256 samples | GDMA descriptor |
| GDMA Descriptors | 6 | Double-buffered ping-pong |
| I2S Mode | Standard (Philips) | BCLK, WS, DIN |
| BCLK | GPIO 4 | pins.h |
| WS | GPIO 5 | pins.h |
| DIN | GPIO 6 | pins.h |

---

## API (`audio_capture.h`)

### `void vaanicore_audio_init(TaskHandle_t notify_task)`
Initializes I2S + GDMA, stores task handle for ISR notification.

### `void vaanicore_audio_read(int16_t *samples, size_t max_samples, size_t *count)`
Reads one frame of audio samples (blocking via task notification).

---

## Implementation Details (`audio_capture.c`)

### I2S Configuration
```c
i2s_std_config_t std_cfg = {
    .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
    .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
    .gpio_cfg = {
        .mclk = I2S_GPIO_UNUSED,
        .bclk = PIN_I2S_BCLK,    // GPIO 4
        .ws = PIN_I2S_WS,        // GPIO 5
        .dout = I2S_GPIO_UNUSED,
        .din = PIN_I2S_DIN,      // GPIO 6
        .invert_flags = {0}
    }
};
```

### GDMA Configuration
```c
// 6 descriptors, each 256 frames (256 × 4 bytes = 1024 bytes per descriptor)
// Total buffer: 6 KB
// Ping-pong: 3 active, 3 being filled
```

### ISR to Task Notification
```c
static bool IRAM_ATTR i2s_rx_callback(i2s_chan_handle_t handle, i2s_event_data_t *event, void *user_ctx) {
    BaseType_t higher_priority_task_woken = pdFALSE;
    vTaskNotifyGiveFromISR(audio_task_handle, &higher_priority_task_woken);
    return higher_priority_task_woken == pdTRUE;
}
```

### Audio Read (32→16 bit saturation)
```c
void vaanicore_audio_read(int16_t *samples, size_t max_samples, size_t *count) {
    size_t bytes_read;
    i2s_channel_read(rx_handle, temp_buf, max_samples * 4, &bytes_read, portMAX_DELAY);
    *count = bytes_read / 4;
    for (size_t i = 0; i < *count; i++) {
        int32_t sample = ((int32_t *)temp_buf)[i];
        // Saturation: clamp to int16_t range
        if (sample > INT16_MAX) sample = INT16_MAX;
        else if (sample < INT16_MIN) sample = INT16_MIN;
        samples[i] = (int16_t)sample;
    }
}
```

---

## Data Flow

```
Microphone (I2S) → GDMA (6×256 descriptors) → ISR → Task Notify → audio_task
                                                                     ↓
                                                              vaanicore_audio_read()
                                                                     ↓
                                                              int16_t[256] → dsp_task (MFCC)
```

---

## Invariants

1. **Sample rate 16kHz** — Matches DSP spec
2. **Mono input** — Single DIN line
3. **32→16 bit saturation** — No wrap-around on overflow
4. **GDMA 6 descriptors** — Continuous capture without gaps
5. **ISR notification** — Zero-copy, low latency
6. **Blocking read** — Task waits for frame via ulTaskNotifyTake
7. **Pin match** — BCLK=4, WS=5, DIN=6 validated against pinmap.csv
8. **FreeRTOS priority** — audio_task priority 6 (highest)

---

## Test Coverage (Host)

| Test | Status |
|------|--------|
| C compilation | ✅ (host-compiled components) |
| Pin validation | ✅ (hardware/validate_pinmap.py) |

## Test Coverage (Hardware - BLOCKED)

| Test | Status |
|------|--------|
| I2S waveform capture | ❌ (requires ESP32-S3 + mic) |
| GDMA descriptor count | ❌ |
| ISR latency | ❌ |
| 32→16 saturation | ❌ |
| Sample rate accuracy | ❌ |
| Buffer overrun/underrun | ❌ |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| I2S init fails | ESP_ERROR_CHECK → abort (boot fail) |
| GDMA alloc fails | ESP_ERROR_CHECK → abort |
| ISR not firing | audio_task blocks forever (watchdog should catch) |
| Buffer overrun | GDMA descriptor overflow (data lost) |
| Sample saturation | Clamped to ±32767 (no wrap) |

---

## Acceptance Criteria

- I2S/GDMA configuration specified with all parameters
- API defined (init, read)
- ISR-to-task notification flow documented
- 32→16 bit saturation algorithm specified
- 8 invariants enumerated
- Hardware tests identified (BLOCKED)
- Next step (0304) can use this output