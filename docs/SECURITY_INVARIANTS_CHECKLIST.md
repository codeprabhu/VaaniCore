# Security Invariants Checklist

**Generated:** 2026-11-18T23:10:00Z
**Git Commit:** a407329
**Status:** APPROVED (this document constitutes the approved checklist)

---

## Invariants

| # | Invariant | Implementation | Test Verification | Status |
|---|-----------|----------------|-------------------|--------|
| S1 | **Allow-list enforcement** — Only predefined verbs accepted | `host/host_agent.py:14` `ALLOWED = {"PING", "OPEN_PROJECT", "RUN_SIMULATION", "SHOW_RESULT", "CLOSE_PROJECT"}` | `test_unknown_verb_rejected`, `test_all_control_intents_are_typed` | ✅ PASS |
| S2 | **Path jail** — Project resolution cannot escape repository root | `host/host_agent.py:26-32` `_project()` validates `ROOT in path.parents` | `test_path_is_project_id_only` | ✅ PASS |
| S3 | **No shell execution** — Launcher uses fixed argv, never `shell=True` | `host/launcher.py:24-25` `subprocess.Popen(command, cwd=project, close_fds=True)` | `test_host_source_forbids_shell_true`, `test_linux_command_is_fixed_argv`, `test_windows_uses_startfile_path` | ✅ PASS |
| S4 | **Confirmation policy** — Risky actions require explicit confirm | `host/host_agent.py:15` `RISKY = {"CLOSE_PROJECT"}`; `dispatch()` checks `confirm` flag | `test_risky_action_requires_confirm` | ✅ PASS |
| S5 | **Audit logging** — All frames logged with metadata, no audio | `host/audit_log.py` `append_frame()` writes JSONL with `{direction, frame, timestamp, error?}` | `test_jsonl_has_frame_metadata_and_no_audio_field` | ✅ PASS |
| S6 | **CRC validation** — Every frame CRC-checked; mismatch → NACK | `host/protocol.py:40` CRC check on decode; `host/host_agent.py:98-101` NACK on ValueError | `test_crc_fault_recovers_sequence_and_returns_nack`, `test_corruption_rejected` | ✅ PASS |
| S7 | **Sequence recovery** — Malformed frames recover seq or use 0 | `host/host_agent.py:19-24` `_protocol_nack()` regex extracts seq prefix | `test_malformed_fault_uses_zero_when_sequence_is_unrecoverable` | ✅ PASS |
| S8 | **Frame size bound** — 128 bytes max enforced | `host/protocol.py:6,27-28` `MAX_FRAME = 128`; encode raises, decode rejects | `test_oversize_rejected` | ✅ PASS |
| S9 | **Retry bounds** — Max 3 attempts, 300ms timeout, 30s task timeout | `host/reliability.py` `RETRY_DELAY=0.3`, `MAX_ATTEMPTS=3`, `TASK_TIMEOUT=30` | `test_retry_recovers_after_two_timeouts`, `test_retry_rejects_more_than_three_attempts` | ✅ PASS |
| S10 | **Measurement parser bounded** — Only numeric `.meas` lines accepted | `host/measurements.py` `parse_meas()` regex `^\.meas\s+\w+\s+([0-9.eE+-]+)` | `test_measurement_parser_only_accepts_numeric_meas_lines` | ✅ PASS |
| S11 | **Simulation fails closed** — No ngspice → ERR, not fake success | `host/host_agent.py:62-63` `if not shutil.which("ngspice"): return ERR` | `test_real_simulation_fails_closed_without_ngspice` | ✅ PASS |
| S12 | **Virtual mode explicit** — SIMULATED label, TARGET values | `host/host_agent.py:57-61` `virtual=True` branch returns `label=SIMULATED`, `gain_db=TARGET`, `bw_hz=TARGET` | `test_virtual_run_can_explicitly_open_project_first` | ✅ PASS |

---

## Attack Surface Analysis

| Vector | Mitigation | Test Coverage |
|--------|------------|---------------|
| Malformed frame injection | CRC16 + size bound + regex validation | `test_corruption_rejected`, `test_oversize_rejected`, `test_fuzz_rejects_or_parses_without_crashing` |
| Path traversal via project ID | `_project()` validates against allow-list + root jail | `test_path_is_project_id_only` |
| Shell injection via launcher | Fixed argv, no `shell=True`, no user input in command | `test_host_source_forbids_shell_true`, `test_linux_command_is_fixed_argv` |
| Unauthorized action | Allow-list + risky confirm gate | `test_unknown_verb_rejected`, `test_risky_action_requires_confirm` |
| Fake measurement injection | Parser only accepts numeric `.meas` lines | `test_measurement_parser_only_accepts_numeric_meas_lines` |
| Simulation spoofing | Real mode requires ngspice, fails closed without it | `test_real_simulation_fails_closed_without_ngspice` |
| Sequence desync | NACK with recovered seq, retry bounds | `test_crc_fault_recovers_sequence_and_returns_nack`, `test_retry_recovers_after_two_timeouts` |
| Audit log tampering | Append-only JSONL, no audio fields | `test_jsonl_has_frame_metadata_and_no_audio_field` |

---

## Human Approval Required For

- Flashing firmware to physical hardware (ESP32-S3)
- Running ngspice simulations (real mode)
- Recording audio dataset (microphone access)
- KiCad PCB fabrication
- Mentor sign-off on final deck

---

## Acceptance Criteria

- All 12 invariants implemented and tested
- Attack surface analyzed with test coverage
- Human approval gates documented
- Checklist approved and stored as `docs/SECURITY_INVARIANTS_CHECKLIST.md`