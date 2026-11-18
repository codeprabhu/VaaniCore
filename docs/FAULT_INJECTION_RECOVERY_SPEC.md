# Fault Injection and Recovery Specification

**Generated:** 2026-11-19T02:25:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** Fault injection test cases and recovery behavior for protocol faults.

**Purpose:** Define how the system handles and recovers from communication faults.

---

## Fault Categories

### 1. CRC Fault
- **Injection:** Flip 1+ bits in CRC field of valid frame
- **Detection:** `decode()` computes CRC over body, compares to frame CRC
- **Recovery:** Host returns NACK with recovered sequence, reason="crc"
- **Device:** Retries frame (up to 3 attempts)

### 2. Malformed Fault (Recoverable Sequence)
- **Injection:** Valid frame with corrupted body (e.g., invalid verb, bad field)
- **Detection:** `decode()` regex/parsing fails after CRC passes
- **Recovery:** Host returns NACK with recovered sequence, reason="malformed"
- **Device:** Retries frame (up to 3 attempts)

### 3. Malformed Fault (Unrecoverable Sequence)
- **Injection:** Random bytes, no `@<digits>:` prefix
- **Detection:** `decode()` fails early, no sequence prefix found
- **Recovery:** Host returns NACK with seq=0, reason="malformed"
- **Device:** Treats as new sequence, retries

### 4. Oversize Frame
- **Injection:** Frame > 128 bytes
- **Detection:** `decode()` length check fails
- **Recovery:** Host returns NACK (seq=0 if no prefix)
- **Device:** Frame dropped (counter incremented)

### 5. Garbage/Fuzz
- **Injection:** Random byte sequences
- **Detection:** `decode()` rejects or parses without crash
- **Recovery:** NACK or valid frame processed
- **Device:** Handles gracefully

---

## Recovery Behavior

### Host Side (`host/host_agent.py:handler`)
```python
try:
    request = decode(line)
    # ... normal processing ...
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

### Device Side (Firmware Retry Logic)
```c
// On NACK received
if (nack.reason == "crc" || nack.reason == "malformed") {
    if (attempt < MAX_ATTEMPTS) {
        vTaskDelay(pdMS_TO_TICKS(RETRY_DELAY_MS));
        resend_frame();
    } else {
        report_error("max retries exceeded");
    }
}
```

---

## Test Cases

| Test | Fault Injected | Expected Recovery |
|------|----------------|-------------------|
| `test_crc_fault_recovers_sequence_and_returns_nack` | Bit flip in CRC | NACK with correct seq, reason="crc" |
| `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | No @<digits>: prefix | NACK seq=0, reason="malformed" |
| `test_corruption_rejected` | Random bit flips | NACK or valid parse, no crash |
| `test_oversize_rejected` | Frame > 128 bytes | NACK (rejected) |
| `test_fuzz_rejects_or_parses_without_crashing` | Random bytes | No crash, NACK or valid |

---

## Invariants

1. **No crash on any input** — Fuzz test verifies
2. **Sequence recovery when possible** — Regex extracts `@<digits>:`
3. **Seq=0 for unrecoverable** — Default when no prefix
4. **Error classification** — CRC vs malformed distinguished
5. **Bounded retries** — Device retries ≤ 3 times
6. **No host retry** — Host is request-response only
7. **Audit log capture** — All faults logged with error context
8. **State consistency** — Host session state unaffected by faults

---

## Test Coverage

| Test | Fault Type | Verifies |
|------|------------|----------|
| `test_crc_fault_recovers_sequence_and_returns_nack` | CRC | Seq recovery, reason="crc" |
| `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | Malformed (no prefix) | Seq=0, reason="malformed" |
| `test_corruption_rejected` | Bit flips | Rejected or parsed, no crash |
| `test_oversize_rejected` | Oversize | Rejected |
| `test_fuzz_rejects_or_parses_without_crashing` | Random | No crash |

---

## Failure Modes

| Fault | Host Response | Device Response | Log Entry |
|-------|---------------|-----------------|-----------|
| CRC error | NACK(seq, "crc") | Retry ×3 | device_to_host (bad), host_to_device (NACK) |
| Malformed (recoverable) | NACK(seq, "malformed") | Retry ×3 | device_to_host (bad), host_to_device (NACK) |
| Malformed (unrecoverable) | NACK(0, "malformed") | Retry ×3 | device_to_host (bad), host_to_device (NACK) |
| Oversize | NACK(0, "malformed") | Drop + counter | host_to_device (NACK) |
| Fuzz (valid parse) | Normal processing | Normal | Normal |
| Fuzz (invalid) | NACK | Retry/Drop | host_to_device (NACK) |

---

## Acceptance Criteria

- 5 fault categories defined with injection/recovery
- Host _protocol_nack() algorithm documented
- Device retry behavior specified
- 5 test cases mapped
- 8 invariants enumerated
- Failure mode table complete
- Next step (0264) can use this output