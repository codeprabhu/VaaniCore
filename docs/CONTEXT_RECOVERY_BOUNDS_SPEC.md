# Context Recovery and Bounds Specification

**Generated:** 2026-11-19T01:45:00Z
**Git Commit:** ae1c35e
**Status:** APPROVED

---

## Contract

**Scope:** Context persistence across restarts, bounded history enforcement, and recovery guarantees.

**Purpose:** Ensure durable, bounded context that survives power cycles and process restarts.

---

## Python ContextStore Recovery (`context_store.py`)

### Initialization
```python
def __init__(self, path: Path | None = None):
    self.path = path or Path.home() / ".vaanicore" / "context.json"
    self.events: list[dict] = []
    self._load()

def _load(self) -> None:
    if self.path.exists():
        with open(self.path) as f:
            data = json.load(f)
        if data.get("schema_version") == 1:
            self.events = data.get("events", [])
```

### Persistence
```python
def _save(self) -> None:
    self.path.parent.mkdir(parents=True, exist_ok=True)
    data = {"schema_version": 1, "events": self.events}
    # TODO: Atomic write (write to temp, rename)
    with open(self.path, "w") as f:
        json.dump(data, f)
```

### Recovery Guarantees
- Survives process restart (file on disk)
- Survives host reboot (file in home directory)
- Schema version for future migration
- Corrupt JSON → exception (no silent corruption)

---

## Firmware NVS Recovery (`nvs_store.c`)

### Initialization
```c
esp_err_t vc_nvs_init(void) {
    esp_err_t err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        err = nvs_flash_init();
    }
    // Load history from NVS
    return vc_nvs_load(&g_history);
}
```

### Persistence
```c
esp_err_t vc_nvs_save(const vc_history_t *history) {
    nvs_handle_t handle;
    esp_err_t err = nvs_open("vaanicore", NVS_READWRITE, &handle);
    if (err != ESP_OK) return err;
    err = nvs_set_blob(handle, "history", history, sizeof(vc_history_t));
    if (err == ESP_OK) err = nvs_commit(handle);
    nvs_close(handle);
    return err;
}
```

### Recovery Guarantees
- Survives power cycle (NVS in flash)
- Survives brownout (NVS atomic commit)
- Survives firmware update (same namespace/key)
- ESP_ERR_NVS_NOT_FOUND → empty history (first boot)
- ESP_ERR_NVS_NO_FREE_PAGES → erase and retry (handled in init)

---

## Bounded History (Both Sides)

| Property | Python | Firmware |
|----------|--------|----------|
| Capacity | 16 events | 16 events |
| Eviction | FIFO (pop(0)) | Circular buffer (next index) |
| Trigger | On append | On append |
| Persistence | On append | On append (or periodic) |

### Python FIFO
```python
self.events.append(event)
if len(self.events) > 16:
    self.events.pop(0)
```

### Firmware Circular Buffer
```c
event = &history->events[history->next];
history->next = (history->next + 1) % 16;
if (history->count < 16) history->count++;
```

---

## Invariants

1. **Bounded at 16** — Both sides enforce hard limit
2. **FIFO semantics** — Oldest event evicted first
3. **Durable persistence** — Python: JSON file; Firmware: NVS flash
4. **Recovery on restart** — Automatic load on init
5. **Atomic NVS write** — ESP-IDF NVS provides commit/rollback
6. **Schema versioning** — Python JSON has schema_version
7. **Corrupt data fails fast** — Exceptions, no silent corruption
8. **Parity** — Both sides same capacity, same event structure

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_history_is_bounded` | Python history capped at 16 |
| `test_sync_and_project_event_resolve_local_day` | Recovery includes local_day |
| `make context-test` | C circular buffer bounds |

---

## Failure Modes

| Condition | Python Behavior | Firmware Behavior |
|-----------|-----------------|-------------------|
| File/NVS missing | Empty history | Empty history |
| Corrupt data | JSONDecodeError → exception | NVS error → empty history |
| Disk/flash full | OSError → exception | ESP_ERR_NVS_NO_FREE_PAGES |
| Schema mismatch | Version check fails → empty | N/A (binary compatible) |
| Power loss during write | Partial write possible (TODO: atomic) | NVS commit atomic |

---

## Acceptance Criteria

- Python recovery via JSON file specified
- Firmware recovery via NVS specified
- Bounded history (16) enforced both sides
- FIFO eviction documented
- 8 invariants enumerated
- Failure modes compared
- Next step (0224) can use this output