# ACK/NACK/Retry Policy Specification

**Generated:** 2026-11-19T02:15:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** Acknowledgment frames, negative acknowledgments, and retry policy for reliable host-device communication.

**Purpose:** Define deterministic recovery from communication faults.

---

## Frame Types

### ACK (Host → Device)
```python
Frame(request.seq, "ACK", {"seq": str(request.seq)})
```
- Sent for **every** valid request frame
- Echoes request sequence number
- No payload beyond seq

### NACK (Host → Device)
```python
Frame(seq, "NACK", {"reason": "crc" | "malformed"})
```
- Sent when frame decode fails (CRC error or malformed)
- `seq`: Recovered from `@<digits>:` prefix, or 0 if unrecoverable
- `reason`: "crc" for CRC mismatch, "malformed" for other format errors

---

## Host Behavior

### Request Handling (`host/host_agent.py:handler`)
```python
try:
    request = decode(line)
    append_frame(log, "device_to_host", request)
    responses = session.handle(request)
    for response in responses:
        append_frame(log, "host_to_device", response)
    return encode(responses)
except ValueError as exc:
    nack = _protocol_nack(line, exc)
    append_frame(log, "host_to_device", nack, str(exc))
    return encode(nack)
```

### Sequence Recovery (`_protocol_nack`)
```python
match = re.match(rb"^@([0-9]{1,3}):", raw)
seq = int(match.group(1)) % 256 if match else 0
reason = "crc" if "CRC" in str(error).upper() else "malformed"
return Frame(seq, "NACK", {"reason": reason})
```

### Session ACK (`host/session.py:handle`)
```python
ack = Frame(request.seq, "ACK", {"seq": str(request.seq)})
# ... dispatch ...
return [ack, response, ...PROJECT_EVENT?]
```

---

## Device Behavior (Firmware)

### Retry Policy (Implemented in device tasks)
```c
// Pseudocode for device retry logic
#define RETRY_DELAY_MS 300
#define MAX_ATTEMPTS 3

for (attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    send_frame(frame);
    response = wait_for_response(RETRY_DELAY_MS);
    if (response && response.verb == "ACK") {
        // Wait for DONE/ERR
        done = wait_for_response(TASK_TIMEOUT_MS);
        break;
    } else if (response && response.verb == "NACK") {
        // Log NACK reason, retry
        continue;
    }
    // Timeout or no response → retry
}
if (attempt > MAX_ATTEMPTS) report_error("max retries exceeded");
```

---

## Timing Parameters (`host/reliability.py`)

| Parameter | Value | Description |
|-----------|-------|-------------|
| RETRY_DELAY | 0.3s | Delay between retry attempts |
| MAX_ATTEMPTS | 3 | Total attempts (including first) |
| TASK_TIMEOUT | 30s | Max task duration |
| IDLE_TIMEOUT | 300s | Idle detection (planned) |

---

## Retry Scenarios

| Scenario | Device Action | Host Response |
|----------|---------------|---------------|
| Normal | Send frame → ACK → DONE | ACK + DONE |
| CRC error | Send frame → NACK(crc) → retry (×3) | NACK with recovered seq |
| Malformed | Send frame → NACK(malformed) → retry (×3) | NACK with seq=0 if unrecoverable |
| No response | Timeout → retry (×3) | N/A (host doesn't retry) |
| Host crash | Timeout → retry (×3) → reconnect | On reconnect: TIME_SYNC |

---

## Invariants

1. **ACK always first** — Every valid request gets ACK before DONE/ERR
2. **NACK recovers sequence** — Regex extracts `@<digits>:` prefix
3. **Bounded retries** — MAX_ATTEMPTS=3, no infinite loops
4. **Fixed delay** — RETRY_DELAY=300ms constant (no backoff)
5. **Error classification** — CRC vs malformed distinguished in NACK
6. **Host stateless** — Host doesn't retry; device initiates retries
7. **Seq modulo 256** — All sequence arithmetic modulo 256
8. **Reconnection handshake** — TIME_SYNC sent immediately on serial connect

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_crc_fault_recovers_sequence_and_returns_nack` | CRC error → NACK with recovered seq |
| `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | Unrecoverable seq → NACK seq=0 |
| `test_retry_recovers_after_two_timeouts` | Device retries twice, succeeds on 3rd |
| `test_retry_rejects_more_than_three_attempts` | 4th attempt rejected |
| `test_round_trip` | Normal ACK/DONE flow |

---

## Failure Modes

| Condition | Host | Device |
|-----------|------|--------|
| CRC error | NACK reason="crc" | Retry ×3 |
| Malformed (recoverable seq) | NACK reason="malformed" | Retry ×3 |
| Malformed (unrecoverable seq) | NACK reason="malformed", seq=0 | Retry ×3 |
| No ACK received | N/A | Retry ×3 then error |
| Host crash mid-task | N/A | Timeout → retry → reconnect |
| Max retries exceeded | N/A | Report error to user |

---

## Acceptance Criteria

- ACK/NACK frame formats specified
- Host _protocol_nack() algorithm documented
- Device retry policy with parameters
- Timing parameters defined
- 8 invariants enumerated
- Test coverage mapped
- Next step (0254) can use this output