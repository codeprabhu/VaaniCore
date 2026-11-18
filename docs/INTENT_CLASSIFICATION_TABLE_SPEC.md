# Intent Classification Table Specification

**Generated:** 2026-11-19T03:25:00Z
**Git Commit:** bc267ff
**Status:** APPROVED

---

## Contract

**Scope:** Firmware intent classification lookup table mapping classifier output to protocol actions.

**Purpose:** Define deterministic intent-to-action mapping for ESP32-S3 firmware.

---

## Intent Definition (`intents.def`)

```
open_amplifier OPEN_PROJECT amplifier 0 0
open_filter OPEN_PROJECT filter 0 0
open_regulator OPEN_PROJECT regulator 0 0
open_last OPEN_PROJECT LAST 0 0
open_yesterday OPEN_PROJECT YESTERDAY 0 0
run_sim RUN_SIMULATION LAST 0 0
open_amp_run_sim RUN_SIMULATION amplifier 0 1
open_yday_run_sim RUN_SIMULATION YESTERDAY 0 1
show_result SHOW_RESULT LAST 0 0
cancel CANCEL "" 0 0
confirm CONFIRM "" 0 0
close_project CLOSE_PROJECT LAST 1 0
_unknown_ "" "" 0 0
_silence_ "" "" 0 0
```

Format: `class_name verb project risky open`

---

## C Structure (`intents.h`)

```c
typedef struct {
    const char *class_name;
    const char *verb;
    const char *project;
    uint8_t risky;
    uint8_t open;
} vc_intent_t;

const vc_intent_t *vc_intent_lookup(const char *class_name);
size_t vc_intent_count(void);
```

---

## Lookup Table (`intents.c`)

```c
static const vc_intent_t INTENTS[] = {
    {"open_amplifier", "OPEN_PROJECT", "amplifier", 0, 0},
    {"open_filter", "OPEN_PROJECT", "filter", 0, 0},
    {"open_regulator", "OPEN_PROJECT", "regulator", 0, 0},
    {"open_last", "OPEN_PROJECT", "LAST", 0, 0},
    {"open_yesterday", "OPEN_PROJECT", "YESTERDAY", 0, 0},
    {"run_sim", "RUN_SIMULATION", "LAST", 0, 0},
    {"open_amp_run_sim", "RUN_SIMULATION", "amplifier", 0, 1},
    {"open_yday_run_sim", "RUN_SIMULATION", "YESTERDAY", 0, 1},
    {"show_result", "SHOW_RESULT", "LAST", 0, 0},
    {"cancel", "CANCEL", "", 0, 0},
    {"confirm", "CONFIRM", "", 0, 0},
    {"close_project", "CLOSE_PROJECT", "LAST", 1, 0},
    {"_unknown_", "", "", 0, 0},
    {"_silence_", "", "", 0, 0},
};
```

### Fields
| Field | Type | Description |
|-------|------|-------------|
| class_name | const char* | Classifier output label (null-terminated) |
| verb | const char* | Protocol verb (PING, OPEN_PROJECT, etc.) |
| project | const char* | Project ID or LAST/YESTERDAY |
| risky | uint8_t | 1 if requires physical confirmation |
| open | uint8_t | 1 if should open project before simulation |

---

## Lookup Function

```c
const vc_intent_t *vc_intent_lookup(const char *class_name) {
    if (!class_name) return NULL;
    for (size_t i = 0; i < sizeof(INTENTS)/sizeof(INTENTS[0]); ++i) {
        if (strcmp(INTENTS[i].class_name, class_name) == 0) return &INTENTS[i];
    }
    return NULL;
}
```

- Linear search (14 entries, negligible)
- Returns NULL for unknown class → treated as _unknown_
- Case-sensitive match

---

## Integration with Firmware Tasks

```c
// intent_task (priority 3, core 1)
void intent_task(void *arg) {
    for (;;) {
        // Wait for classifier output (class_name string)
        char class_name[32];
        if (xQueueReceive(classifier_queue, &class_name, portMAX_DELAY)) {
            const vc_intent_t *intent = vc_intent_lookup(class_name);
            if (intent && intent->verb[0]) {
                // Build frame
                char fields[64] = {0};
                if (intent->project[0]) {
                    snprintf(fields, sizeof(fields), "project=%s", intent->project);
                    if (intent->open) {
                        strncat(fields, ",open=1", sizeof(fields)-strlen(fields)-1);
                    }
                }
                char frame[128];
                vaanicore_encode_frame(next_seq++, intent->verb, fields[0]?fields:NULL, frame, sizeof(frame));
                // Send to comms_task queue
                xQueueSend(comms_tx_queue, frame, 0);
            }
        }
    }
}
```

---

## Special Intents

| Intent | Behavior |
|--------|----------|
| `_unknown_` | Classifier output not in table → no frame sent (or ERR) |
| `_silence_` | VAD detected silence → no frame sent |
| `cancel` | Sends CANCEL frame |
| `confirm` | Sends CONFIRM frame (for risky fallback) |
| `close_project` | Risky=1, requires confirm |

---

## Invariants

1. **Closed vocabulary** — Only 13 defined intents + 2 special
2. **Project allow-list** — All projects in {amplifier, filter, regulator, LAST, YESTERDAY}
3. **Risky flag** — Only CLOSE_PROJECT has risky=1
4. **Open flag** — Only RUN_SIMULATION variants have open=1
5. **Deterministic lookup** — Linear search, exact string match
6. **No heap** — Static const table, no allocation
7. **Classifier agnostic** — Table maps any classifier output labels
8. **Test vectors** — `tests/intents_c.c` validates table structure

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make intent-test` | C intent table structure correct |
| `test_all_control_intents_are_typed` | Verbs in allow-list |
| `test_supported_phrase` | Python phrase mapping |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Classifier outputs unknown label | `_unknown_` → no action |
| Classifier outputs silence | `_silence_` → no action |
| Lookup returns NULL | Treated as `_unknown_` |
| Project not in allow-list | Host will reject (ERR:invalid_project_id) |

---

## Acceptance Criteria

- Intent table defined with 13 intents + 2 special
- C structure and lookup function specified
- Integration with firmware tasks shown
- Special intents documented
- 8 invariants enumerated
- Test coverage mapped
- Next step (0324) can use this output