# Device Protocol Context Specification

**Generated:** 2026-11-19T01:25:00Z
**Git Commit:** ae1c35e
**Status:** APPROVED

---

## Contract

**Scope:** Python mirror of firmware device context for virtual device testing.

**Purpose:** Enable host-side simulation of device context state for integration testing.

---

## DeviceContext Class (`firmware/components/context/device_protocol.py`)

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
Processes host-to-device frames:
- **TIME_SYNC:** Updates `epoch`, `tz_offset_min`, computes `local_day`
- **PROJECT_EVENT:** Appends event to history with current `local_day`

```python
if frame.verb == "TIME_SYNC":
    self.epoch = int(frame.fields["epoch"])
    self.tz_offset_min = int(frame.fields["tz_offset_min"])
    self.local_day = (self.epoch + self.tz_offset_min * 60) // 86400
elif frame.verb == "PROJECT_EVENT":
    event = {
        "project_id": frame.fields["project"],
        "action": frame.fields["action"],
        "local_day": self.local_day
    }
    self.history.append(event)
    if len(self.history) > 16:
        self.history.pop(0)
```

#### `get_last() -> dict | None`
Returns `self.history[-1]` if history non-empty.

#### `get_yesterday() -> dict | None`
Returns event with `local_day == self.local_day - 1` if exactly one match.

---

## Local Day Computation

```python
local_day = (epoch + tz_offset_min * 60) // 86400
```
- Integer days since Unix epoch in local timezone
- Updated on every TIME_SYNC
- Used for PROJECT_EVENT timestamp and YESTERDAY resolution

---

## Integration with Virtual Device

```python
# virtual_device.py
device = DeviceContext()

# Connection handshake
for frame in session.connect_frames():  # [TIME_SYNC]
    device.handle(frame)

# Request/response loop
for request in requests:
    for response in session.handle(request):
        device.handle(response)  # Updates context on PROJECT_EVENT
```

---

## Invariants

1. **Mirrors firmware** — Behavior matches `context.c` exactly
2. **Bounded history** — 16 events max, FIFO
3. **Time sync required** — `local_day` valid only after TIME_SYNC
4. **No persistence** — In-memory only (virtual testing)
4. **Deterministic** — Same frame sequence → same context state
5. **No LAST/YESTERDAY resolution** — Host resolves; device only stores

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_history_is_bounded` | History capped at 16 |
| `test_sync_and_project_event_resolve_local_day` | TIME_SYNC sets day, PROJECT_EVENT uses it |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| TIME_SYNC not received | `local_day=0`, PROJECT_EVENT uses day 0 |
| PROJECT_EVENT before TIME_SYNC | Event logged with day 0 |
| History full | Oldest event dropped (FIFO) |
| Unknown frame verb | Ignored (no-op) |

---

## Acceptance Criteria

- DeviceContext class specified with handle, get_last, get_yesterday
- Local day computation documented
- Virtual device integration shown
- 5 invariants enumerated
- Test coverage mapped
- Next step (0204) can use this output