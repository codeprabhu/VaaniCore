# Context Store Python Specification

**Generated:** 2026-11-19T01:05:00Z
**Git Commit:** ae1c35e
**Status:** APPROVED

---

## Contract

**Scope:** Python context store for host-side and virtual device context persistence.

**Purpose:** Provide durable, bounded, inspectable project/task context with LAST/YESTERDAY resolution.

---

## ContextStore Class (`firmware/components/context/context_store.py`)

### Storage
- **File:** `~/.vaanicore/context.json` (created on first use)
- **Format:** JSON with `events` list and `schema_version`
- **Schema:**
```json
{
  "schema_version": 1,
  "events": [
    {"project_id": "amplifier", "action": "RUN_SIMULATION", "local_day": 12345}
  ]
}
```

### History Bounds
- **Capacity:** 16 events (FIFO, oldest dropped)
- **Persistence:** Written on every `append()`

### Methods

#### `append(project_id: str, action: str, local_day: int) -> None`
Adds event to history, persists to disk.
```python
event = {"project_id": project_id, "action": action, "local_day": local_day}
events.append(event)
if len(events) > 16:
    events.pop(0)
save()
```

#### `get_last() -> dict | None`
Returns most recent event or None if empty.

#### `get_yesterday(today: int) -> dict | None`
Returns event with `local_day == today - 1` if exactly one exists.

#### `resolve(selector: str, today: int, confirmed_fallback: bool = False) -> dict | None`
Resolves LAST or YESTERDAY selector.
```python
if selector == "LAST":
    return get_last()
elif selector == "YESTERDAY":
    matches = [e for e in events if e["local_day"] == today - 1]
    if len(matches) == 1:
        return matches[0]
    if confirmed_fallback and events:
        return events[-1]  # fallback to LAST
    return None
return None
```

---

## DeviceContext Class (`firmware/components/context/device_protocol.py`)

Virtual device mirror of firmware context for testing.

### State
```python
class DeviceContext:
    def __init__(self):
        self.history: list[dict] = []  # Max 16 events
        self.epoch: int = 0
        self.tz_offset_min: int = 0
        self.local_day: int = 0
```

### Methods

#### `handle(frame: Frame) -> None`
Processes host frames:
- **TIME_SYNC:** Sets `epoch`, `tz_offset_min`, computes `local_day`
- **PROJECT_EVENT:** Appends `{"project_id", "action", "local_day"}` to history (max 16)

#### `get_last() -> dict | None`
Returns `history[-1]` if exists.

#### `get_yesterday() -> dict | None`
Returns event with `local_day == self.local_day - 1` if unique.

---

## Local Day Computation

```python
# From TIME_SYNC epoch + tz_offset_min
local_day = (epoch + tz_offset_min * 60) // 86400
```
- Integer day number since Unix epoch in local timezone
- Used for YESTERDAY resolution

---

## Invariants

1. **Bounded history** — Maximum 16 events, FIFO eviction
2. **Durable persistence** — JSON file written on every append
3. **LAST always works** — Returns most recent if history non-empty
4. **YESTERDAY requires uniqueness** — Multiple events same day → None (unless confirmed_fallback)
5. **Confirmed fallback** — `confirmed_fallback=True` allows LAST as YESTERDAY fallback
6. **Time sync required** — `local_day` only valid after TIME_SYNC
7. **Schema versioning** — `schema_version` in JSON for future migration
8. **Atomic writes** — Write to temp file, then rename (not yet implemented, noted)

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_last` | LAST returns most recent event |
| `test_yesterday` | YESTERDAY returns previous day event |
| `test_missing_yesterday_requires_confirmation` | Non-unique yesterday returns None without fallback |
| `test_history_is_bounded` | History capped at 16 events |
| `test_sync_and_project_event_resolve_local_day` | TIME_SYNC sets day, PROJECT_EVENT uses it |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Context file missing | Created on first append |
| Context file corrupt | Exception raised, no silent corruption |
| Disk full on write | Exception raised |
| TIME_SYNC not received | `local_day` = 0, YESTERDAY resolution fails |
| Selector unknown | Returns None |

---

## Acceptance Criteria

- ContextStore class specified with all methods
- Storage format and bounds defined
- DeviceContext mirror specified
- Local day computation documented
- 8 invariants enumerated
- Test coverage mapped
- Next step (0184) can use this output