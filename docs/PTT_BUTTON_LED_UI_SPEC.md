# PTT Button and LED UI Specification

**Generated:** 2026-11-19T03:35:00Z
**Git Commit:** bc267ff
**Status:** APPROVED (scaffold complete, hardware validation BLOCKED)

---

## Contract

**Scope:** Physical UI (buttons, LEDs, mute switch) for ESP32-S3 firmware.

**Purpose:** Define button/LED behavior for push-to-talk and status indication.

---

## GPIO Assignments (`pins.h`)

| Signal | GPIO | Type | Config |
|--------|------|------|--------|
| BUTTON_CONFIRM | 15 | Input | Pull-up, interrupt any edge |
| BUTTON_ABORT | 16 | Input | Pull-up, interrupt any edge |
| MUTE_SENSE | 17 | Input | Pull-up, interrupt any edge (privacy switch) |
| LED_LISTEN | 18 | Output | Push-pull, initial low |
| LED_BUSY | 21 | Output | Push-pull, initial low |
| LED_ERR | 47 | Output | Push-pull, initial low |

---

## UI Events (`ui.h`)

```c
typedef enum {
    VC_UI_EVENT_CONFIRM_PRESS,
    VC_UI_EVENT_CONFIRM_RELEASE,
    VC_UI_EVENT_ABORT_PRESS,
    VC_UI_EVENT_ABORT_RELEASE,
    VC_UI_EVENT_MUTE_ON,
    VC_UI_EVENT_MUTE_OFF,
} vc_ui_event_type_t;

typedef struct {
    vc_ui_event_type_t type;
    uint32_t timestamp_ms;
} vc_ui_event_t;
```

---

## API

### `void vc_ui_init(QueueHandle_t event_queue)`
Initializes GPIOs, configures interrupts, stores event queue.

### `void vc_ui_set_led(vc_ui_led_t led, bool on)`
Sets LED state (listen, busy, err).

### `void vc_ui_set_led_pattern(vc_ui_led_t led, vc_ui_pattern_t pattern)`
Sets LED pattern (solid, blink, blink_fast, off).

---

## Button Behavior

### Push-to-Talk (PTT)
- **Primary:** BUTTON_CONFIRM (GPIO15) — Press to start capture, release to stop
- **Abort:** BUTTON_ABORT (GPIO16) — Press to cancel current action
- **Debounce:** Software in ui_task (50ms typical)

### Mute Switch (Privacy)
- **MUTE_SENSE** (GPIO17) — Hardware privacy switch
- **On:** Microphone electrically disconnected (external circuit)
- **Firmware:** Reports MUTE_ON/MUTE_OFF events, blocks capture if muted

### Event Flow
```
Button press/release → GPIO ISR → vc_ui_event_t → ui_events_queue (xQueueSendFromISR)
                                                                     ↓
                                                              ui_task (xQueueReceive)
                                                                     ↓
                                                              Debounce (50ms)
                                                                     ↓
                                                CONFIRM → intent_task (CONFIRM frame)
                                                ABORT → intent_task (CANCEL frame)
                                                MUTE → comms_task (blocks capture)
```

---

## LED Patterns

| LED | Pattern | Meaning |
|-----|---------|---------|
| LISTEN (GPIO18) | Blink 1Hz | Waiting for PTT / ready |
| LISTEN | Solid | Capturing audio (PTT held) |
| BUSY (GPIO21) | Solid | Processing (DSP/ML/comms) |
| ERR (GPIO47) | Blink fast 5Hz | Error (CRC, comms, hardware) |
| ERR | Solid | Fatal error |

---

## OLED Display (Not Implemented)

- **Status:** Placeholder only
- **I2C:** SDA=GPIO8, SCL=GPIO9 (pins.h)
- **Driver:** Not present in scaffold
- **Future:** Status text, waveform, menu

---

## API Details (`ui.c`)

```c
void vc_ui_init(QueueHandle_t event_queue) {
    // Configure button GPIOs: input, pull-up, interrupt any edge
    // Configure LED GPIOs: output, initial low
    // Install ISR handlers → queue events
}

void vc_ui_isr_handler(void *arg) {
    // Determine which GPIO triggered
    // Create vc_ui_event_t with type + timestamp
    // xQueueSendFromISR(event_queue, &event, &higher_priority_task_woken)
}

void ui_task(void *arg) {
    vc_ui_event_t event;
    for (;;) {
        xQueueReceive(ui_events_queue, &event, portMAX_DELAY);
        // Debounce: ignore if <50ms since last same button event
        // Route event:
        //   CONFIRM_PRESS → intent_task (start capture)
        //   CONFIRM_RELEASE → intent_task (stop capture, classify)
        //   ABORT_PRESS → intent_task (CANCEL)
        //   MUTE_ON/OFF → comms_task (block/enable capture)
    }
}
```

---

## Invariants

1. **PTT on CONFIRM** — Primary capture trigger
2. **Abort on ABORT** — Immediate cancellation
3. **Mute hardware-enforced** — External circuit disconnects mic
4. **Mute reported** — Firmware knows mute state
5. **LED patterns distinct** — Listen/busy/err unambiguous
6. **ISR minimal** — Only queues event, no processing
7. **Debounce in task** — 50ms software debounce
8. **OLED absent** — Documented as not implemented

---

## Test Coverage (Host)

| Test | Status |
|------|--------|
| C compilation | ✅ |
| Pin validation | ✅ (hardware/validate_pinmap.py) |

## Test Coverage (Hardware - BLOCKED)

| Test | Status |
|------|--------|
| Button press/release detection | ❌ |
| Debounce effectiveness | ❌ |
| LED pattern visibility | ❌ |
| Mute switch detection | ❌ |
| ISR latency | ❌ |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Button stuck pressed | Debounce ignores, capture starts once |
| Button stuck released | Capture stops normally |
| Mute switch floating | Pull-up ensures defined state |
| LED GPIO conflict | Pin validation catches at build |
| ISR queue full | Event dropped (rare, small queue) |

---

## Acceptance Criteria

- GPIO assignments match pins.h and pinmap.csv
- Button events defined (press/release for confirm/abort, on/off for mute)
- LED patterns specified (listen/busy/err)
- UI task flow with ISR and debounce documented
- OLED absence noted
- 8 invariants enumerated
- Hardware validation BLOCKED
- Next step (0334) can use this output