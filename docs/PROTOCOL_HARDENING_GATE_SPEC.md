# Protocol Hardening Gate Specification

**Generated:** 2026-11-19T02:45:00Z
**Git Commit:** afb3795
**Status:** APPROVED

---

## Contract

**Scope:** Consolidated protocol hardening verification across all Phase 4 workstreams.

**Purpose:** Confirm host and device recover safely from communication faults.

---

## Hardening Checklist

| Area | Specification | Test | Status |
|------|---------------|------|--------|
| **Frame Encoding** | `vaanicore_encode_frame` / `host/protocol.py:encode` | `make protocol-test`, `test_round_trip` | ✅ PASS |
| **Frame Decoding** | `vaanicore_decode_frame` / `host/protocol.py:decode` | `make protocol-test`, `test_shared_vectors` | ✅ PASS |
| **CRC16 Parity** | CRC-16/CCITT-FALSE identical Python/C | `test_crc_known_vector`, `test_shared_vectors` | ✅ PASS |
| **ACK Policy** | Every request → ACK first | `test_round_trip`, `test_session` | ✅ PASS |
| **NACK Recovery** | CRC/malformed → NACK with recovered seq | `test_crc_fault_recovers_sequence_and_returns_nack`, `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | ✅ PASS |
| **Retry Policy** | Device: 3 attempts, 300ms delay | `test_retry_recovers_after_two_timeouts`, `test_retry_rejects_more_than_three_attempts` | ✅ PASS |
| **Fault Handling** | CRC, malformed, oversize, fuzz | `test_corruption_rejected`, `test_oversize_rejected`, `test_fuzz_rejects_or_parses_without_crashing` | ✅ PASS |
| **Transport** | 1s read timeout, TIME_SYNC on connect | `test_discovery_is_safe_without_serial_dependency`, `test_serial_unplug_reconnects_and_repeats_handshake` | ✅ PASS |
| **Session Sequencing** | Seq modulo 256, ACK+DONE/ERR+PROJECT_EVENT | `test_connect_has_time_sync`, `test_success_emits_ack_done_and_project_event` | ✅ PASS |
| **Size Bounds** | 128 bytes max frame | `test_oversize_rejected` | ✅ PASS |

---

## Gate Criteria (All Must Pass)

| Criterion | Evidence |
|-----------|----------|
| C encode/decode matches Python | `make protocol-test` → "C protocol vector passed" |
| CRC16 vectors match | `test_crc_known_vector` PASS |
| ACK for every request | `test_round_trip` PASS |
| NACK recovers sequence | `test_crc_fault_recovers_sequence_and_returns_nack` PASS |
| Malformed uses seq=0 | `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` PASS |
| Retry recovers after 2 timeouts | `test_retry_recovers_after_two_timeouts` PASS |
| Retry rejects 4th attempt | `test_retry_rejects_more_than_three_attempts` PASS |
| Corruption rejected | `test_corruption_rejected` PASS |
| Oversize rejected | `test_oversize_rejected` PASS |
| Fuzz safe | `test_fuzz_rejects_or_parses_without_crashing` PASS |
| Discovery safe | `test_discovery_is_safe_without_serial_dependency` PASS |
| Reconnection handshake | `test_serial_unplug_reconnects_and_repeats_handshake` PASS |
| Full test suite passes | `make test` → 50 tests OK |

---

## Unresolved Items (Deferred to Hardware)

| Item | Reason |
|------|--------|
| Task timeout enforcement (30s) | Not implemented in code; defined in reliability.py |
| Idle detection (300s) | Not implemented; planned |
| Automatic reconnection | Requires host process manager (systemd) |
| Cross-device clock estimation | `[[HUMAN: measure on hardware]]` |
| Physical layer fault injection | Requires hardware (cable unplug, noise) |

---

## Invariants (Consolidated from Phase 4)

1. **No heap in C codec** — Bounded stack buffers only
2. **CRC on every frame** — Encode adds, decode verifies
3. **ACK always first** — Before DONE/ERR
4. **NACK recovers sequence** — Regex `@<digits>:` or 0
5. **Bounded retries** — MAX_ATTEMPTS=3, fixed 300ms delay
6. **Error classification** — CRC vs malformed
7. **Size bound** — 128 bytes max
8. **Seq modulo 256** — All arithmetic wrapped
9. **Python/C parity** — Verified for protocol, context, DSP, intents
10. **Safe discovery** — Returns None, no crash
11. **TIME_SYNC on connect** — Immediate handshake
12. **Host stateless** — No host-side retry

---

## Acceptance Criteria

- All 13 gate criteria pass
- Unresolved items explicitly documented
- 12 consolidated invariants
- Phase 4 complete
- Next step (0284) can use this output