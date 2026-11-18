# Session and Time Sync Specification

**Generated:** 2026-11-19T00:05:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Connection lifecycle, sequence management, time synchronization, and response handling for the host agent.

**Purpose:** Define session behavior for reliable host-device communication.

---

## HostSession Class

### State
```python
class HostSession:
    def __init__(self, virtual: bool = False):
        self.virtual = virtual
        self.next_seq = 1              # Next sequence number to assign (1-255, modulo 256)
        self.last_result: dict | None  # Cached RUN_SIMULATION result for SHOW_RESULT
```

### Methods

#### `time_sync() -> Frame`
Generates TIME_SYNC frame with current epoch and timezone offset.
```python
Frame(seq=next_seq % 256, "TIME_SYNC", {
    "epoch": str(int(time.time())),
    "tz_offset_min": str(offset)  # UTC offset in minutes, e.g., 330 for IST
})
```

#### `connect_frames() -> list[Frame]`
Returns frames to send on new connection.
```python
[time_sync()]  # Single TIME_SYNC frame
```

#### `handle(request: Frame, confirm: bool = False) -> list[Frame]`
Processes incoming request frame, returns response frames.
```python
ack = Frame(request.seq, "ACK", {"seq": str(request.seq)})
if request.verb == "SHOW_RESULT":
    if last_result is None:
        response = Frame(request.seq, "ERR", {"code": "no_result_available"})
    else:
        response = Frame(request.seq, "DONE", dict(last_result))
else:
    response = dispatch(request, confirm=confirm, virtual=virtual)
    if request.verb == "RUN_SIMULATION" and response.verb == "DONE":
        last_result = {k: v for k, v in response.fields.items()
                       if k in {"status", "project", "gain_db", "bw_hz", "label"}}

frames = [ack, response]
if response.verb == "DONE" and response.fields.get("project") \
   and request.verb in {"OPEN_PROJECT", "RUN_SIMULATION"}:
    frames.append(Frame(request.seq, "PROJECT_EVENT",
                       {"action": request.verb, "project": response.fields["project"],
                        "epoch": str(int(time.time()))}))
return frames
```

---

## Sequence Number Management

- **Range:** 1-255 (0 reserved for error frames without recoverable seq)
- **Allocation:** `next_seq` incremented after each use, modulo 256
- **Recovery:** NACK includes recovered sequence from malformed frame prefix
- **Device-side:** Device tracks sequence for responses (ACK/NACK/DONE/ERR)

---

## Time Synchronization

### Host → Device (TIME_SYNC)
- Sent immediately on connection (stdio or serial)
- Contains: `epoch` (Unix timestamp), `tz_offset_min` (minutes from UTC)
- Device uses to set local clock and compute `local_day` for context

### Device → Host
- No time sync frames from device
- Device includes `local_day` in PROJECT_EVENT if needed (future)

### Clock Estimation
- Cross-device clock estimation error: `[[HUMAN: measure on hardware]]`
- Not currently measured; marked as human action

---

## Response Sequencing

For every request, host sends (in order):
1. **ACK** — Acknowledges receipt with original sequence
2. **DONE/ERR** — Result of dispatch
3. **PROJECT_EVENT** (conditional) — If DONE and project-related verb

---

## Result Caching

- **Cached:** Only RUN_SIMULATION success responses
- **Keys kept:** status, project, gain_db, bw_hz, label
- **Used by:** SHOW_RESULT verb
- **Lifetime:** Session duration (cleared on new HostSession)

---

## PROJECT_EVENT Frame

```python
Frame(seq, "PROJECT_EVENT", {
    "action": "OPEN_PROJECT" | "RUN_SIMULATION",
    "project": "amplifier" | "filter" | "regulator",
    "epoch": str(int(time.time()))
})
```
- Sent to device for context synchronization
- Device updates `DeviceContext` history via `handle()`

---

## Invariants

1. **Seq modulo 256** — All sequence numbers wrapped
2. **ACK always first** — Every request gets ACK before DONE/ERR
3. **TIME_SYNC on connect** — No other frames before TIME_SYNC
4. **Result cache isolation** — Only RUN_SIMULATION populates cache
5. **PROJECT_EVENT only on success** — ERR responses don't emit events
6. **Virtual mode flag** — Passed through to dispatch for SIMULATED label

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| SHOW_RESULT with no cache | Returns ERR:no_result_available |
| Dispatch returns ERR | ACK + ERR sent, no PROJECT_EVENT |
| Seq overflow (255→1) | Modulo arithmetic handles automatically |
| TIME_SYNC timestamp invalid | Not validated (trusted host clock) |

---

## Acceptance Criteria

- Session class specified with all methods
- Sequence management defined
- Time sync protocol specified
- Response sequencing documented
- Result caching behavior defined
- PROJECT_EVENT format specified
- 6 invariants enumerated
- Next step (0124) can use this output