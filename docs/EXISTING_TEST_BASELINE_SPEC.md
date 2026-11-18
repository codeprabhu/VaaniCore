# Existing Test Baseline Specification

## Contract

**Scope:** Python tests, C protocol/context/DSP/intent tests, and CI commands.

**Purpose:** Capture current test behavior, classify any failures, establish baseline for regression detection.

## Inputs

- Test source files in `tests/`
- Source code under test in `host/`, `firmware/components/`, `firmware/main/`
- Makefile test targets
- CI environment (GitHub Actions implied by README)

## Outputs

- Test baseline report with:
  - Test inventory by category
  - Pass/fail status for each test
  - Failure classification (if any): flaky, environmental, genuine regression
  - Coverage gaps identified
  - CI command verification

## Invariants

1. **No test weakening:** Existing tests must not be modified to pass; only new tests added
2. **Honest labeling:** Simulated vs measured clearly distinguished
3. **Reproducibility:** `make test` must produce same results
4. **Isolation:** Test changes don't affect production code

## Failure Behavior

- If tests fail → classify failure, do not mask
- If test depends on unavailable tool (ESP-IDF, ngspice) → mark as expected skip/block
- If flaky → document and investigate

## Test Categories

### Protocol Tests (7 tests)
- `test_crc_known_vector` - CRC16-CCITT-FALSE against known vectors
- `test_round_trip` - encode/decode round-trip
- `test_corruption_rejected` - bit-flip corruption detected
- `test_oversize_rejected` - >128 byte frames rejected
- `test_fuzz_rejects_or_parses_without_crashing` - random input handling
- `test_retry_recovers_after_two_timeouts` - retry policy (3 attempts, 300ms)
- `test_retry_rejects_more_than_three_attempts` - max retries enforced
- `test_shared_vectors` - Python/C vector parity

### Context Tests (3 tests)
- `test_last` - LAST selector resolves to most recent event
- `test_yesterday` - YESTERDAY selector resolves to previous day
- `test_missing_yesterday_requires_confirmation` - fallback requires confirm

### DSP Tests (3 tests)
- `test_golden_vector_is_reproducible` - Python features deterministic
- `test_shape` - MFCC output shape correct
- `test_two_second_window_has_124_frames` - framing math correct
- C parity: max_abs_error=0.0139313

### Intent Tests (3 tests)
- `test_all_control_intents_are_typed` - control verbs in allow-list
- `test_supported_phrase` - phrase_to_frame maps known phrases
- `test_unknown_phrase_never_becomes_action` - unknown → ERR

### Security Tests (7 tests)
- `test_host_source_forbids_shell_true` - no shell=True in host_agent
- `test_measurement_parser_only_accepts_numeric_meas_lines` - parser bounded
- `test_path_is_project_id_only` - path jail enforced
- `test_real_simulation_fails_closed_without_ngspice` - safe default
- `test_risky_action_requires_confirm` - CLOSE_PROJECT needs confirm
- `test_unknown_verb_rejected` - allow-list enforcement
- `test_virtual_run_can_explicitly_open_project_first` - open flag works

### Session Tests (4 tests)
- `test_connect_has_time_sync` - TIME_SYNC frame on connect
- `test_error_has_no_project_event` - ERR doesn't emit PROJECT_EVENT
- `test_show_result_requires_and_then_returns_cached_result` - SHOW_RESULT flow
- `test_success_emits_ack_done_and_project_event` - success flow

### Transport Tests (2 tests)
- `test_discovery_is_safe_without_serial_dependency` - no crash without serial
- `test_serial_unplug_reconnects_and_repeats_handshake` - reconnection logic

### Virtual Device Tests (1 test)
- `test_session_sync_and_event_update_device_context` - full loop

### Launcher Tests (2 tests)
- `test_linux_command_is_fixed_argv` - xdg-open fixed argv
- `test_windows_uses_startfile_path` - os.startfile on Windows

### ML Eval Gate Tests (1 test)
- `test_missing_metadata_writes_non_result_status` - eval gate blocks incomplete

### Audit/FMEA/Hardware/Deck/Baseline/Dataset/Timing Tests (22 tests)
- Various validation and structural tests

## CI Commands (from Makefile)

```make
test: protocol-test context-test dsp-test intent-test
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

protocol-test:  # C protocol vectors
context-test:   # C context vectors
dsp-test:       # C DSP parity
intent-test:    # C intent table
```

## Acceptance Criteria

- Test baseline report generated
- All 50 tests pass (current status)
- Failure classifications documented (none currently)
- Next step (0014) can use this output