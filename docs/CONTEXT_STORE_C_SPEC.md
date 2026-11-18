# Context Store C Firmware Specification

**Generated:** 2026-11-19T01:15:00Z
**Git Commit:** ae1c35e
**Status:** APPROVED

---

## Contract

**Scope:** C firmware context store with NVS persistence for ESP32-S3.

**Purpose:** Provide durable, bounded context on device matching Python behavior.

---

## Data Structures

### `vc_event_t` (context.h)
```c
typedef struct {
    char project_id[32];
    char action[32];
    int32_t local_day;
} vc_event_t;
```

### `vc_history_t` (context.h)
```c
#define VAANICORE_HISTORY_CAPACITY 16

typedef struct {
    vc_event_t events[VAANICORE_HISTORY_CAPACITY];
    uint8_t next;      // Next write index (0-15)
    uint8_t count;     // Number of valid events (0-16)
} vc_history_t;
```

---

## API (`context.h`)

### `void vc_history_init(vc_history_t *history)`
Initializes history to empty (zeroes all fields).

### `void vc_history_append(vc_history_t *history, const char *project_id, const char *action, int32_t local_day)`
Appends event to circular buffer.
```c
vc_event_t *event = &history->events[history->next];
memset(event, 0, sizeof(*event));
strncpy(event->project_id, project_id ? project_id : "", 31);
strncpy(event->action, action ? action : "", 31);
event->local_day = local_day;
history->next = (history->next + 1) % 16;
if (history->count < 16) history->count++;
```

### `int vc_history_resolve(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out)`
Resolves LAST or YESTERDAY (no fallback).
- Returns 1 on success, 0 on failure
- LAST: returns most recent event (`events[(next-1+16)%16]`)
- YESTERDAY: scans for `local_day == today-1`, returns if unique

### `int vc_history_resolve_confirmed(const vc_history_t *history, const char *selector, int32_t today, vc_event_t *out)`
Resolves with confirmed fallback for YESTERDAY.
- If YESTERDAY not unique but `confirmed_fallback=true`, returns LAST

---

## NVS Store (`nvs_store.h`)

### `esp_err_t vc_nvs_init(void)`
Initializes NVS partition, loads history into global `vc_history_t`.

### `esp_err_t vc_nvs_save(const vc_history_t *history)`
Saves history to NVS namespace "vaanicore", key "history".

### `esp_err_t vc_nvs_load(vc_history_t *history)`
Loads history from NVS. Returns ESP_ERR_NVS_NOT_FOUND if empty.

---

## Integration Points

### Firmware Main (`main.c`)
```c
// On boot
vc_nvs_init();

// On PROJECT_EVENT frame received
vc_history_append(&history, project_id, action, local_day);
vc_nvs_save(&history);  // Or periodic save

// On intent classification with LAST/YESTERDAY
vc_event_t event;
if (vc_history_resolve_confirmed(&history, selector, local_day, &event)) {
    // Use event.project_id for action
}
```

### Local Day Tracking
- Device maintains `local_day` from last TIME_SYNC
- Updated on each TIME_SYNC frame received
- Used for YESTERDAY resolution

---

## Invariants

1. **Bounded history** — Fixed 16-event circular buffer, no dynamic allocation
2. **NVS persistence** — Survives power cycle, brownout, reset
3. **Python parity** — Resolution logic matches `context_store.py` exactly
4. **No heap allocation** — All buffers stack/static
5. **Strncpy bounds** — 31 char + null terminator for strings
6. **Atomic NVS write** — ESP-IDF NVS provides atomicity
7. **Schema compatibility** — Same field names as Python JSON
8. **Test vectors** — `tests/context_c.c` validates against known vectors

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make context-test` | C context vectors match Python |
| `tests/context_c.c` | LAST, YESTERDAY, confirmed fallback, bounds |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| NVS not initialized | `vc_nvs_init()` must be called first |
| NVS partition full | `vc_nvs_save()` returns ESP_ERR_NVS_NO_FREE_PAGES |
| History corrupt in NVS | `vc_nvs_load()` returns error, history starts empty |
| Selector unknown | `vc_history_resolve` returns 0 |
| Today not set (no TIME_SYNC) | YESTERDAY resolution fails (local_day=0) |

---

## Acceptance Criteria

- C data structures defined (vc_event_t, vc_history_t)
- API specified with exact behavior
- NVS store integration specified
- Firmware integration points documented
- 8 invariants enumerated
- Test coverage mapped
- Next step (0194) can use this output