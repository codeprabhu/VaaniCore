# Host Reliability and Retries Specification

**Generated:** 2026-11-19T00:45:00Z
**Git Commit:** b213b2d
**Status:** APPROVED

---

## Contract

**Scope:** Retry policy, timeout handling, error recovery, and fault tolerance for host-device communication.

**Purpose:** Define bounded, deterministic reliability behavior for the serial link.

---

## Configuration (`host/reliability.py`)

```python
RETRY_DELAY = 0.3        # 300ms between retry attempts
MAX_ATTEMPTS = 3         # Maximum retry attempts (including first)
TASK_TIMEOUT = 30.0      # 30 second max task duration
IDLE_TIMEOUT = 300.0     # 5 minute idle detection (not yet enforced)
```

---

## Error Handling

### CRC Error Recovery
```python
# host/host_agent.py:_protocol_nack()
def _protocol_nack(raw: bytes, error: Exception) -> Frame:
    match = re.match(rb"^@([0-9]{1,3}):", raw)
    seq = int(match.group(1)) % 256 if match else 0
    reason = "crc" if "CRC" in str(error).upper() else "malformed"
    return Frame(seq, "NACK", {"reason": reason})
```

- Recovers sequence from `@<digits>:` prefix if present
- Defaults to seq=0 if no recoverable prefix
- Classifies error as "crc" or "malformed"

### Malformed Frame Handling
- Oversize (>128 bytes) → ValueError → NACK reason="malformed"
- Invalid CRC → ValueError → NACK reason="crc"
- Missing newline → ValueError → NACK reason="malformed"
- Invalid field format → ValueError → NACK reason="malformed"

---

## Retry Policy (Device-Side)

Device firmware implements retry logic:

| Attempt | Action |
|---------|--------|
| 1 | Send frame, wait for ACK |
| 2 | If no ACK after RETRY_DELAY, resend |
| 3 | If no ACK after 2×RETRY_DELAY, resend |
| 4+ | Abort, report error to user |

**Host does not retry** — Host is request-response; device initiates retries.

---

## Timeout Handling

### Task Timeout (30s)
- Maximum duration for any host-side operation (ngspice, launcher)
- Not yet enforced in code; defined for future implementation

### Serial Read Timeout
- `serve_serial()` uses pyserial timeout (configurable)
- Default: 1 second read timeout

### Reconnection
- On serial disconnect: `serve_serial()` exits
- Host restart required (systemd/service manager responsibility)
- On reconnect: `on_connect` callback sends TIME_SYNC immediately

---

## Idle Detection (Planned)

```python
# In reliability.py (not yet enforced)
IDLE_TIMEOUT = 300.0  # 5 minutes no activity
# Future: send PING, expect DONE, else reconnect
```

---

## Invariants

1. **Bounded retries** — MAX_ATTEMPTS=3, no infinite retry loops
2. **Fixed delay** — RETRY_DELAY=300ms constant, no exponential backoff
3. **Sequence recovery** — NACK includes recovered seq or 0
4. **Error classification** — CRC vs malformed distinguished
5. **Task timeout defined** — 30s maximum (enforcement pending)
6. **Reconnection handshake** — TIME_SYNC sent immediately on connect
7. **No host-side retry** — Host is stateless request-response
8. **Garbage frame drop** — Oversize/malformed frames dropped with counters (device-side)

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_crc_fault_recovers_sequence_and_returns_nack` | CRC error → NACK with recovered seq |
| `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | Unrecoverable seq → NACK seq=0 |
| `test_retry_recovers_after_two_timeouts` | Device retries twice, succeeds on 3rd |
| `test_retry_rejects_more_than_three_attempts` | 4th attempt rejected |
| `test_corruption_rejected` | Bit-flip corruption detected |
| `test_oversize_rejected` | >128 byte frames rejected |
| `test_fuzz_rejects_or_parses_without_crashing` | Random input handled safely |

---

## Acceptance Criteria

- Retry policy parameters defined
- Error handling flow documented
- Sequence recovery algorithm specified
- Timeout values defined
- 8 invariants enumerated
- Test coverage mapped
- Next step (0164) can use this output