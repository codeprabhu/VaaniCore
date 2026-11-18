# FMEA Test Matrix Specification

**Generated:** 2026-11-19T05:55:00Z
**Git Commit:** ae74c9b
**Status:** APPROVED

---

## Contract

**Scope:** Failure Mode and Effects Analysis with test case mapping for VaaniCore prototype.

**Purpose:** Ensure all identified failure modes have corresponding test coverage.

---

## FMEA Structure (`docs/FMEA.csv`)

| Column | Description |
|--------|-------------|
| id | Unique failure mode ID (FM-001 to FM-020) |
| component | Subsystem (protocol, transport, host, firmware, hardware, ml) |
| failure_mode | Description of failure |
| effect | User-visible effect |
| cause | Root cause |
| severity | 1-10 (10 = catastrophic) |
| occurrence | 1-10 (10 = frequent) |
| detection | 1-10 (10 = undetectable) |
| rpn | Risk Priority Number (S×O×D) |
| mitigation | Design/test mitigation |

### 20 Failure Modes (Summary)

| ID | Component | Failure Mode | RPN |
|----|-----------|--------------|-----|
| FM-001 | protocol | CRC error undetected | 120 |
| FM-002 | protocol | Malformed frame accepted | 100 |
| FM-003 | protocol | Sequence desync | 90 |
| FM-004 | transport | Serial disconnect | 150 |
| FM-005 | transport | Port discovery fails | 80 |
| FM-006 | host | Unknown verb executed | 60 |
| FM-007 | host | Path escape | 200 |
| FM-008 | host | Shell injection | 200 |
| FM-009 | host | Risky action without confirm | 120 |
| FM-010 | host | Fake simulation result | 100 |
| FM-011 | firmware | Audio capture fails | 150 |
| FM-012 | firmware | MFCC compute error | 120 |
| FM-013 | firmware | Intent misclassification | 100 |
| FM-014 | firmware | Context loss on reset | 80 |
| FM-015 | firmware | NVS corruption | 90 |
| FM-016 | hardware | Button stuck | 60 |
| FM-017 | hardware | LED failure | 40 |
| FM-018 | hardware | Mute switch failure | 80 |
| FM-019 | ml | Model accuracy too low | 120 |
| FM-020 | ml | Quantization accuracy drop | 100 |

---

## Test Mapping (`docs/FMEA_TEST_MAP.csv`)

| fmea_id | test_case_id | test_file |
|---------|--------------|-----------|
| FM-001 | test_crc_fault_recovers_sequence_and_returns_nack | test_host_protocol_faults.py |
| FM-002 | test_malformed_fault_uses_zero_when_sequence_is_unrecoverable | test_host_protocol_faults.py |
| FM-003 | test_retry_recovers_after_two_timeouts | test_protocol.py |
| FM-004 | test_serial_unplug_reconnects_and_repeats_handshake | test_transport.py |
| FM-005 | test_discovery_is_safe_without_serial_dependency | test_transport.py |
| FM-006 | test_unknown_verb_rejected | test_security.py |
| FM-007 | test_path_is_project_id_only | test_security.py |
| FM-008 | test_host_source_forbids_shell_true | test_security.py |
| FM-009 | test_risky_action_requires_confirm | test_security.py |
| FM-010 | test_real_simulation_fails_closed_without_ngspice | test_security.py |
| FM-011 | (hardware) | — |
| FM-012 | make dsp-test | — |
| FM-013 | (requires dataset) | — |
| FM-014 | make context-test | — |
| FM-015 | (requires hardware) | — |
| FM-016 | (hardware) | — |
| FM-017 | (hardware) | — |
| FM-018 | (hardware) | — |
| FM-019 | (requires dataset) | — |
| FM-020 | (requires trained model) | — |

---

## Validation (`tools/validate_fmea.py`)

```python
def validate_fmea():
    # 1. Check FMEA.csv has required columns
    # 2. Check severity/occurrence/detection in 1-10
    # 3. Check RPN = S × O × D
    # 4. Check FMEA_TEST_MAP.csv maps all FMEA IDs
    # 3. Report coverage gaps
```

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_all_rows_have_evidence_mapping` | All 20 FMEA rows have test mapping |

---

## Invariants

1. **Complete mapping** — Every FMEA row has test_case_id in map
2. **RPN correct** — RPN = Severity × Occurrence × Detection
3. **Test traceability** — test_case_id maps to actual test function
4. **Coverage honest** — Hardware/ML failures marked as requiring hardware/data
5. **Risk prioritization** — High RPN items have test coverage
5. **Validation automated** — validate_fmea.py in make audit

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_all_rows_have_evidence_mapping` | All 20 FMEA rows mapped |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| FMEA row unmapped | validate_fmea.py reports gap |
| RPN miscalculated | Validation fails |
| Test case missing | Gap reported |
| Hardware failure untested | Marked as requiring hardware |

---

## Acceptance Criteria

- FMEA.csv with 20 failure modes documented
- FMEA_TEST_MAP.csv maps all to tests
- validate_fmea.py validates structure
- Test coverage gap identified (hardware/ML blocked)
- 6 invariants enumerated
- Next step (0534) can use this output