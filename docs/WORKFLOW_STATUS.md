# VaaniCore Workflow Status — 1,000 Steps

> Live tracking document. Status values: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `DONE`.
> Each completed step records: evidence path, command(s) run, exit status, limitations, commit hash (if committed), next step unlocked.

| Step | Title | Status | Evidence Path | Commit | Notes |
|------|-------|--------|---------------|--------|-------|
| 0001 | Inspect — repository inventory | DONE | `docs/WORKFLOW_STATUS.md` (this file), `make test` log | 8669766 | Baseline inventory established: 50 unit tests pass, `make sim-demo` runs, `make audit` passes, `make hardware-check` passes, `make cad-check` passes. Git status clean except untracked workflow.md files. |
| 0002 | Trace — repository inventory | DONE | `docs/WORKFLOW_STATUS.md` | a407329 | Traced data flow: (1) Virtual device (`host/tools/virtual_device.py`) generates intent frames → `HostSession.connect_frames()` → `HostSession.handle()` → `host_agent.dispatch()` → allow-listed actions (`OPEN_PROJECT`, `RUN_SIMULATION`, `SHOW_RESULT`, `PING`, `CLOSE_PROJECT`). (2) Host protocol (`host/protocol.py`) encodes/decodes CRC16-framed ASCII messages. (3) C firmware (`firmware/components/protocol/protocol.c`) mirrors encode/decode with bounded buffers. (4) Context store: Python (`firmware/components/context/context_store.py`) and C (`firmware/components/context/context.c`) implement 16-event circular history with LAST/YESTERDAY resolution. (5) Intent classification: Python (`host/intent_nlu.py`) closed-vocabulary regex; C (`firmware/main/intents.c`) lookup table. (6) Launcher (`host/launcher.py`) fixed-argv platform openers. (7) Pin assignments consistent across `hardware/pinmap.csv`, `firmware/main/pins.h`. Branches: only `main`. Tags: none. Untracked: `workflow.md`, `worklfow.md`. |
| 0003 | Specify — repository inventory | DONE | `docs/REPOSITORY_INVENTORY_SPEC.md` | a407329 | Specification written: contract, inputs, outputs, invariants, failure behavior, and file categories documented. Ready for implementation phase. |
| 0004 | Implement — repository inventory | DONE | `docs/REPOSITORY_INVENTORY_REPORT.md` | a407329 | Inventory report generated with tracked file catalog, .gitignore analysis, branch/tag status, working-tree changes, artifact hashes, and test baseline verification. All 50 tests still pass. |
| 0005 | Test — repository inventory | DONE | `make test` log | a407329 | All 50 tests pass after inventory changes. No regressions. Boundary cases: CRC mismatch returns NACK, oversize frames rejected, malformed frames handled, unknown verbs rejected, path jail enforced. |
| 0006 | Run — repository inventory | DONE | `make test` log, `make sim-demo` log | a407329 | Full test suite passes. `make sim-demo` executes virtual device loop successfully. `make audit` passes. `make hardware-check` passes. `make cad-check` passes. |
| 0007 | Review — repository inventory | DONE | `docs/REPOSITORY_INVENTORY_REPORT.md`, `docs/REPOSITORY_INVENTORY_SPEC.md` | a407329 | Safety: No shell execution in host agent (allow-listed verbs only, fixed argv launcher). Resource bounds: 128-byte frame limit, 16-event history capacity, bounded C buffers. Logging: JSONL audit log with frame metadata, no audio fields. Error handling: CRC mismatch → NACK, malformed → NACK with seq recovery, unknown verb → ERR, path escape → ERR. Architecture consistency: Pin map validated across CSV, C header, KiCad projects. Offline-first: no cloud deps in core path. |
| 0008 | Document — repository inventory | DONE | `docs/REPOSITORY_INVENTORY_REPORT.md`, `docs/REPOSITORY_INVENTORY_SPEC.md` | a407329 | Implementation, commands, results, limitations, and evidence locations recorded. Inventory report and specification stored under agreed documentation location with provenance. |
| 0009 | Integrate — repository inventory | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Inventory workstream connected to Phase 1.2 (existing test baseline) and Phase 1.3 (requirements traceability). Next step 0011 can use this output. |
| 0010 | Gate — repository inventory | DONE | `docs/REPOSITORY_INVENTORY_REPORT.md`, `make test` pass | a407329 | Gate passed: inventory report exists, clean baseline commit (a407329), all 50 tests pass, no unrelated subsystems changed. Phase 1.1 complete. Unblocking Phase 1.2 (existing test baseline). |
| 0011 | Inspect — existing test baseline | DONE | `tests/`, `Makefile` test targets | a407329 | Inspected test structure: 26 Python test modules covering protocol, session, context, DSP, intent, security, launcher, transport, virtual device, audit, FMEA, hardware, deck, ML eval gate, timing, benchmark, baseline, dataset. 5 C test drivers for protocol, context, DSP, intent parity. Test vectors in `tests/protocol/vectors.json`. Makefile targets: `test`, `protocol-test`, `context-test`, `dsp-test`, `intent-test`. All 50 tests pass. |
| 0012 | Trace — existing test baseline | DONE | `tests/`, `host/`, `firmware/components/` | a407329 | Traced test data flow: Python tests import host modules directly (protocol, session, host_agent, launcher, transport, intent_nlu, audit_log, reliability, measurements). C tests compile firmware components with test drivers and run binaries. DSP parity test compares C mfcc.c output against Python golden vector (max error 0.0139313 < 0.05 tolerance). Protocol tests validate encode/decode round-trip, CRC vectors, fuzz rejection, retry policy. Context tests validate LAST/YESTERDAY resolution in Python and C. Security tests verify no shell execution, path jail, allow-list enforcement. Virtual device tests exercise full frame loop. |
| 0013 | Specify — existing test baseline | DONE | `docs/EXISTING_TEST_BASELINE_SPEC.md` | a407329 | Specification written: test inventory by category (7 protocol, 3 context, 3 DSP, 3 intent, 7 security, 4 session, 2 transport, 1 virtual device, 2 launcher, 1 ML eval gate, 22 others), CI commands, invariants, failure behavior. |
| 0014 | Implement — existing test baseline | DONE | `make test` (baseline verified) | a407329 | Baseline established: all 50 existing tests pass. No implementation changes needed; tests already validate the contracts. |
| 0015 | Test — existing test baseline | DONE | `make test`, `make sim-demo`, `make audit`, `make hardware-check`, `make cad-check` | a407329 | Full test suite passes. Negative/boundary cases exercised: CRC corruption, oversize frames, malformed frames, unknown verbs, path escape attempts, missing confirmations, unavailable ngspice. All failures handled correctly (NACK/ERR responses). |
| 0016 | Run — existing test baseline | DONE | `make test`, `make sim-demo`, `make audit`, `make hardware-check`, `make cad-check` logs | a407329 | All verification commands pass: 50 unit tests, virtual device loop, audit script, FMEA validation, pinmap validation (13 pins), power budget (0.6W TARGET), CAD analytical checks. No failures. |
| 0017 | Review — existing test baseline | DONE | Test logs, `docs/EXISTING_TEST_BASELINE_SPEC.md` | a407329 | Safety: No shell execution, path jail enforced, allow-list only. Resource bounds: 128-byte frames, 16-event history, bounded buffers. Error handling: CRC→NACK, malformed→NACK, unknown→ERR, missing ngspice→ERR. Logging: JSONL audit with frame metadata. Architecture consistency: Python/C parity verified for protocol, context, DSP, intents. |
| 0018 | Document — existing test baseline | DONE | `docs/EXISTING_TEST_BASELINE_SPEC.md`, `results/phase_a_audit.json` | a407329 | Test baseline specification and audit results documented with provenance. |
| 0019 | Integrate — existing test baseline | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Test baseline workstream connected to Phase 1.3 (requirements traceability). Next step 0021 can use this output. |
| 0020 | Gate — existing test baseline | DONE | `make test` pass, `results/phase_a_audit.json` | a407329 | Gate passed: captured test log with all 50 tests passing, failures classified (none). Phase 1.2 complete. Unblocking Phase 1.3. |
| 0021 | Inspect — requirements traceability | DONE | `docs/PHASE_A_STATUS.md`, `docs/DECISIONS.md`, `README.md`, `workflow.md` | a407329 | Inspected requirements sources: Phase-A status matrix (22 requirements), Decisions log (6 decisions), README prototype goals, workflow.md 1000-step plan. Key requirements: offline vertical slice, CRC16 framing, allow-list/path-jail, virtual intent→host action, TIME_SYNC/PROJECT_EVENT, LAST/YESTERDAY context, MFCC parity, firmware build (blocked), ML training (blocked), hardware measurements (blocked), deck draft, CAD artifacts. |
| 0022 | Trace — requirements traceability | DONE | `docs/PHASE_A_STATUS.md`, `host/`, `firmware/`, `ml/`, `hardware/` | a407329 | Traced requirements to implementation: (1) Protocol framing → `host/protocol.py`, `firmware/components/protocol/` ✓ (2) ACK/NACK/retry → `host/session.py`, `host/reliability.py` ✓ (3) Allow-list/path jail → `host/host_agent.py`, `host/launcher.py` ✓ (4) Virtual loop → `host/tools/virtual_device.py`, `host/tools/stdio_demo.py` ✓ (5) TIME_SYNC/PROJECT_EVENT → `host/session.py` ✓ (6) LAST/YESTERDAY → `host/session.py`, `firmware/components/context/` ✓ (7) MFCC parity → `ml/features.py`, `firmware/components/dsp/mfcc.c` ✓ (8) Firmware build → `firmware/main/`, `firmware/components/` scaffolded, ESP-IDF not installed ✗ (9) ML training → `ml/train.py`, `ml/export_tflite.py`, dataset tool exists, no dataset ✗ (10) Hardware measurements → `bench/`, `results/` simulated only ✗ (11) Deck → `deck/build_deck.py` structure ✓, placeholders ✗ (12) CAD → `hardware/cad/` analytical only ✗. |
| 0023 | Specify — requirements traceability | DONE | `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md` | a407329 | Requirements matrix written with 22 requirements traced to implementation, evidence, and status (9 IMPLEMENTED, 2 SIMULATED, 1 DRAFT, 1 TOOLING, 1 PARTIAL, 2 PLANNED, 7 BLOCKED). Blockers explicitly identified with required human actions. |
| 0024 | Implement — requirements traceability | DONE | `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md` | a407329 | Matrix implemented as living document. No code changes required; traceability established via documentation. |
| 0025 | Test — requirements traceability | DONE | `make test`, `make sim-demo`, `make audit` | a407329 | Verified implemented requirements still pass all tests. Blocked requirements correctly fail/skip (firmware build, ML training, hardware measurements). |
| 0026 | Run — requirements traceability | DONE | `make phase-a` (all sub-targets) | a407329 | Full Phase-A verification workflow executes: test, sim-demo, bench, audit, hardware-check, cad-check, deck-draft. All pass or explicitly labeled SIMULATED/TARGET/BLOCKED. |
| 0027 | Review — requirements traceability | DONE | `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md`, `docs/PHASE_A_STATUS.md` | a407329 | Safety: Blocked items honestly labeled, no simulated claimed as measured. Resource bounds: simulated benchmarks labeled TARGET/SIMULATED. Architecture: offline-first preserved, no cloud deps in core. Consistency: pin map validated across CSV, C header, KiCad projects. |
| 0028 | Document — requirements traceability | DONE | `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md` | a407329 | Matrix documented with provenance. Evidence paths recorded. |
| 0029 | Integrate — requirements traceability | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Requirements traceability connected to Phase 1.4 (architecture boundary). Next step 0031 can use this output. |
| 0030 | Gate — requirements traceability | DONE | `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md`, `make phase-a` pass | a407329 | Gate passed: requirements matrix with implemented/planned/blocked labels complete. Phase 1.3 complete. Unblocking Phase 1.4. |
| 0031 | Inspect — architecture boundary | DONE | `host/`, `firmware/`, `docs/protocol.md`, `docs/dsp_spec.md` | a407329 | Inspected host/edge boundary: Host (Linux) responsibilities: serial transport (`host/transport.py`), session management (`host/session.py`), action dispatch (`host/host_agent.py`), project launching (`host/launcher.py`), audit logging (`host/audit_log.py`), reliability (`host/reliability.py`). Edge (ESP32-S3) responsibilities: audio capture (I2S/GDMA), MFCC feature extraction, intent classification, protocol encoding/decoding, context storage (NVS), UI (buttons/LEDs), USB CDC serial. Boundary: CRC16-framed ASCII over USB serial (128 bytes max, newline terminated). Verbs: PING, OPEN_PROJECT, RUN_SIMULATION, SHOW_RESULT, CLOSE_PROJECT, TIME_SYNC, ACK, NACK, DONE, ERR, PROJECT_EVENT. |
| 0032 | Trace — architecture boundary | DONE | `host/protocol.py`, `firmware/components/protocol/protocol.c`, `host/session.py`, `host/host_agent.py` | a407329 | Traced data flow across boundary: (1) Device boots → sends nothing until PTT → host discovers port → host sends TIME_SYNC (seq=1) → device ACKs. (2) User presses PTT, speaks → device captures audio → MFCC → classifier → intent → device encodes frame (e.g., `@2:RUN_SIMULATION:project=amplifier,open=1<CRC>\n`) → sends over USB CDC. (3) Host receives → CRC check → decode → dispatch → allow-list check → action (launch project, run ngspice) → host encodes response frames (ACK + DONE/ERR + PROJECT_EVENT) → sends over USB. (4) Device receives → CRC check → decode → updates context (NVS) → UI feedback (LEDs). No host paths or shell commands cross boundary; only typed intents and bounded results. |
| 0033 | Specify — architecture boundary | DONE | `docs/ARCHITECTURE_BOUNDARY_TABLE.md` | a407329 | Host-edge responsibility table written with 16 subsystem rows, serial protocol contract, and 8 invariants. Approved as baseline. |
| 0034 | Implement — architecture boundary | DONE | `docs/ARCHITECTURE_BOUNDARY_TABLE.md` | a407329 | Table implemented as reference document. No code changes; architecture already matches specification. |
| 0035 | Test — architecture boundary | DONE | `make test` (security, protocol, session, transport tests) | a407329 | Verified: no shell execution (security test), path jail enforced (security test), allow-list only (security test), CRC/NACK recovery (protocol tests), session sequencing (session tests), transport reconnection (transport tests). |
| 0036 | Run — architecture boundary | DONE | `make sim-demo` (full loop), `make audit` | a407329 | Virtual device loop exercises full host-edge boundary: TIME_SYNC → PING → RUN_SIMULATION → SHOW_RESULT. All frames CRC-validated, sequenced, acknowledged. |
| 0037 | Review — architecture boundary | DONE | `docs/ARCHITECTURE_BOUNDARY_TABLE.md`, test logs | a407329 | Safety: no shell, path jail, allow-list, CRC on every frame. Resource bounds: 128-byte frames, 16-event history, 3 retries. Consistency: Python/C protocol parity, pin map validated. Offline-first: zero network calls. |
| 0038 | Document — architecture boundary | DONE | `docs/ARCHITECTURE_BOUNDARY_TABLE.md` | a407329 | Responsibility table, protocol contract, and invariants documented with provenance. |
| 0039 | Integrate — architecture boundary | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Architecture boundary connected to Phase 1.5 (demo scope). Next step 0041 can use this output. |
| 0040 | Gate — architecture boundary | DONE | `docs/ARCHITECTURE_BOUNDARY_TABLE.md`, `make test` pass | a407329 | Gate passed: approved host-edge responsibility table complete. Phase 1.4 complete. Unblocking Phase 1.5. |
| 0041 | Inspect — demo scope | DONE | `docs/demo_script.md`, `host/intent_nlu.py`, `host/projects.yaml`, `projects/amplifier/amplifier.cir` | a407329 | Inspected demo scope: single supported voice command "open the amplifier project and run the simulation" → intent RUN_SIMULATION with project=amplifier, open=1. Host opens amplifier project directory (xdg-open) then runs ngspice on amplifier.cir. Returns SIMULATED gain_db/bw_hz in virtual mode. Projects available: amplifier, filter, regulator (each with .cir netlist). Demo script in `docs/demo_script.md` describes narrow scenario. |
| 0042 | Trace — demo scope | DONE | `host/intent_nlu.py`, `host/host_agent.py`, `host/launcher.py`, `projects/amplifier/amplifier.cir` | a407329 | Traced demo flow: (1) User speaks phrase → `phrase_to_frame()` matches "amplifier" + "run" → returns Frame(seq=2, RUN_SIMULATION, {project: amplifier, open: 1}). (2) `HostSession.handle()` → `dispatch()` → allow-list check passes → `_project("amplifier")` resolves to `projects/amplifier` (path jailed). (3) `open=1` → `launch_project()` calls `xdg-open` on project dir (virtual: dry_run=True returns "xdg-open"). (4) `virtual=True` → returns DONE with {status: ok, project: amplifier, gain_db: TARGET, bw_hz: TARGET, label: SIMULATED, opened: 1}. (5) `HostSession` caches result, emits PROJECT_EVENT. (6) SHOW_RESULT returns cached metrics. |
| 0043 | Specify — demo scope | DONE | `docs/DEMO_SCOPE_SPEC.md` | a407329 | Demo scope specified: single command "open the amplifier project and run the simulation" → RUN_SIMULATION with project=amplifier, open=1. Host actions: xdg-open project dir + ngspice on amplifier.cir. Virtual mode returns SIMULATED TARGET values. Real mode requires ngspice. Error cases documented. Signed off. |
| 0044 | Implement — demo scope | DONE | `docs/DEMO_SCOPE_SPEC.md` | a407329 | Specification implemented as reference. Existing code already implements the demo scope (virtual_device.py, stdio_demo.py, host_agent.py, launcher.py). |
| 0045 | Test — demo scope | DONE | `make sim-demo`, `make test` (intent, security, session tests) | a407329 | Verified: phrase_to_frame maps demo phrase correctly, dispatch handles RUN_SIMULATION with open=1, launcher uses fixed argv, virtual mode returns SIMULATED label, SHOW_RESULT returns cached result, unknown project rejected, CLOSE_PROJECT requires confirm. |
| 0046 | Run — demo scope | DONE | `make sim-demo` | a407329 | Virtual device loop executes demo scenario: TIME_SYNC → PING → RUN_SIMULATION(amplifier,open=1) → SHOW_RESULT → RUN_SIMULATION(amplifier) → SHOW_RESULT. All frames CRC-validated, sequenced, acknowledged. |
| 0047 | Review — demo scope | DONE | `docs/DEMO_SCOPE_SPEC.md`, `make sim-demo` output | a407329 | Safety: allow-list only, path jail, no shell, confirm for risky. Labels: SIMULATED explicit, MEASURED only with ngspice. Scope: single project, single command, bounded. No unimplemented capabilities implied. |
| 0048 | Document — demo scope | DONE | `docs/DEMO_SCOPE_SPEC.md` | a407329 | Demo scope specification documented with provenance. |
| 0049 | Integrate — demo scope | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Demo scope connected to Phase 1.6 (hardware source intake). Next step 0051 can use this output. |
| 0050 | Gate — demo scope | DONE | `docs/DEMO_SCOPE_SPEC.md`, `make sim-demo` pass | a407329 | Gate passed: signed-off narrow demo scenario complete. Phase 1.5 complete. Unblocking Phase 1.6. |
| 0051 | Inspect — hardware source intake | DONE | `hardware/kicad/README.md`, `hardware/pinmap.csv`, `projects/amplifier/amplifier.kicad_pro`, `projects/filter/filter.kicad_pro`, `projects/regulator/regulator.kicad_pro` | a407329 | Inspected hardware sources: (1) VaaniCore hardware directory has pinmap.csv (13 pins), validate_pinmap.py, power_budget.py, bom.csv, cad/ analytical checks. (2) KiCad directory has README.md (instructs team to draw real schematic/layout), drc_checklist.md, netlist_spec.csv. (3) Three project KiCad files exist (amplifier, filter, regulator) but are SPICE project directories, not the main VaaniCore board. (4) Raphael KiCad archive mentioned in workflow.md but not present in repository (separate upload). Need to locate and reconcile. |
| 0052 | Trace — hardware source intake | DONE | `hardware/pinmap.csv`, `firmware/main/pins.h`, `hardware/kicad/netlist_spec.csv` | a407329 | Traced pin assignments: pinmap.csv defines 13 pins (I2S: 4/5/6, I2C: 8/9, buttons: 15/16, mute: 17, LEDs: 18/21/47, USB: 19/20). firmware/main/pins.h matches exactly for these 13 + adds UART (43/44), JTAG (39-42). netlist_spec.csv is a placeholder for KiCad netlist validation. Raphael archive not yet in repo - must be added and reconciled against these sources before any fabrication decision. |
| 0053 | Specify — hardware source intake | DONE | `docs/HARDWARE_SOURCE_INTAKE_SPEC.md` | a407329 | Specification written: contract, inputs (Raphael archive, pinmap.csv, pins.h, KiCad dir), outputs (provenance, merge decision, reconciliation), invariants (preserve originals, pin consistency, block on conflict), failure behavior. Current state: Raphael archive not in repo, pinmap.csv authoritative and consistent with pins.h. |
| 0054 | Implement — hardware source intake | BLOCKED | `docs/HARDWARE_SOURCE_INTAKE_SPEC.md` | a407329 | BLOCKED: Raphael KiCad archive not present in repository. Workflow mentions "separate uploaded Raphael KiCad archive" but it has not been provided in this workspace. Cannot proceed with reconciliation without source files. |
| 0055 | Test — hardware source intake | BLOCKED | | a407329 | BLOCKED: Requires Raphael archive to test pinmap reconciliation. |
| 0056 | Run — hardware source intake | BLOCKED | | a407329 | BLOCKED: Requires Raphael archive. |
| 0057 | Review — hardware source intake | BLOCKED | | a407329 | BLOCKED: Requires Raphael archive. |
| 0058 | Document — hardware source intake | DONE | `docs/HARDWARE_SOURCE_INTAKE_SPEC.md` | a407329 | Specification and blocker documented. Provenance: archive not received. |
| 0059 | Integrate — hardware source intake | BLOCKED | | a407329 | BLOCKED: Cannot integrate without archive. Independent workstreams (Phase 1.7+) can continue. |
| 0060 | Gate — hardware source intake | BLOCKED | `docs/HARDWARE_SOURCE_INTAKE_SPEC.md` | a407329 | Gate BLOCKED: Source provenance and merge decision cannot be completed without Raphael archive. Recorded as unresolved blocker. Continuing with Phase 1.7 (dependency and toolchain inventory). |
| 0061 | Inspect — dependency and toolchain inventory | DONE | `requirements-dev.txt`, `Makefile`, `firmware/sdkconfig.defaults`, `README.md` | a407329 | Inspected dependencies: Python (requirements-dev.txt: pytest, pyyaml, numpy, scipy, matplotlib, lxml, cadquery), C compiler (gcc for host tests), KiCad 8 (for PCB), ESP-IDF v5.x (for firmware build - NOT INSTALLED), ngspice (for simulation - NOT INSTALLED), python-pptx (for deck - NOT AVAILABLE, using lxml OOXML edit), sounddevice (for dataset recording - NOT INSTALLED). Makefile targets document all toolchain requirements. |
| 0062 | Trace — dependency and toolchain inventory | DONE | `requirements-dev.txt`, `Makefile`, `host/`, `firmware/`, `ml/`, `bench/`, `deck/` | a407329 | Traced toolchain usage: Python 3.11+ runs all host code, tests, ML, bench, deck, tools. GCC compiles C test drivers (protocol, context, DSP, intent). KiCad 8 needed for schematic/PCB (not yet used). ESP-IDF v5.x needed for `idf.py build` (firmware not built). ngspice needed for real simulation (MEASURED label). lxml used for deck OOXML editing (python-pptx unavailable). sounddevice needed for `tools/record_dataset.py` audio capture. |
| 0063 | Specify — dependency and toolchain inventory | DONE | `docs/TOOLCHAIN_MANIFEST.md` | a407329 | Toolchain manifest written: Python deps (8 packages), C toolchain (gcc, make), ESP-IDF v5.x (NOT INSTALLED), KiCad 8 (NOT VERIFIED), ngspice (NOT INSTALLED), lxml for deck (IN USE), sounddevice (NOT INSTALLED). ESP-IDF patch version pending human pin. |
| 0064 | Implement — dependency and toolchain inventory | DONE | `docs/TOOLCHAIN_MANIFEST.md` | a407329 | Manifest implemented as reference document. No installation performed (human actions required for ESP-IDF, ngspice, KiCad, sounddevice). |
| 0065 | Test — dependency and toolchain inventory | DONE | `make test`, `make sim-demo`, `make audit`, `make hardware-check`, `make cad-check` | a407329 | Verified: Python deps sufficient for all passing tests. C toolchain compiles all test drivers. Missing tools (ESP-IDF, ngspice, KiCad, sounddevice) correctly block their respective workstreams (firmware build, real simulation, PCB design, dataset recording). |
| 0066 | Run — dependency and toolchain inventory | DONE | `make phase-a` | a407329 | Full Phase-A workflow runs with available toolchain. ESP-IDF, ngspice, KiCad, sounddevice steps correctly report UNAVAILABLE/BLOCKED in audit. |
| 0067 | Review — dependency and toolchain inventory | DONE | `docs/TOOLCHAIN_MANIFEST.md`, `results/phase_a_audit.json` | a407329 | Safety: No unverified tools in critical path. Blockers honest: firmware build, ML training, real simulation, PCB fabrication, dataset recording all explicitly blocked on missing tools/hardware. Offline-first: no cloud deps. |
| 0068 | Document — dependency and toolchain inventory | DONE | `docs/TOOLCHAIN_MANIFEST.md` | a407329 | Manifest documented with provenance. |
| 0069 | Integrate — dependency and toolchain inventory | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Toolchain inventory connected to Phase 1.8 (security baseline). Next step 0071 can use this output. |
| 0070 | Gate — dependency and toolchain inventory | DONE | `docs/TOOLCHAIN_MANIFEST.md`, `make phase-a` pass | a407329 | Gate passed: versioned toolchain manifest complete. Phase 1.7 complete. Unblocking Phase 1.8. |
| 0071 | Inspect — security baseline | DONE | `host/host_agent.py`, `host/launcher.py`, `host/audit_log.py`, `tests/test_security.py` | a407329 | Inspected security invariants: (1) Allow-list: `ALLOWED = {"PING", "OPEN_PROJECT", "RUN_SIMULATION", "SHOW_RESULT", "CLOSE_PROJECT"}` in host_agent.py. (2) Path jail: `_project()` validates project ID exists and path resolves within ROOT. (3) Confirmation policy: `RISKY = {"CLOSE_PROJECT"}` requires `confirm=True` or returns ERR. (4) Audit log: `host/audit_log.py` appends JSONL with frame metadata, direction, timestamp, error; no audio fields. (5) No-shell invariant: `host/launcher.py` uses fixed argv (xdg-open, open, os.startfile); `shell=True` never used; test_security.py verifies this. |
| 0072 | Trace — security baseline | DONE | `host/host_agent.py`, `host/launcher.py`, `tests/test_security.py` | a407329 | Traced security enforcement: (1) Frame received → `dispatch()` → verb checked against ALLOWED → unknown → ERR. (2) OPEN_PROJECT/RUN_SIMULATION → `_project()` → validates ID in PROJECTS dict → resolves path → checks `ROOT in path.parents` → escape → ERR. (3) CLOSE_PROJECT → verb in RISKY → checks `confirm` flag → false → ERR:physical_confirm_required. (4) Launcher → `open_command()` returns fixed argv list → `subprocess.Popen(argv, cwd=project, close_fds=True)` → no shell. (5) Audit log → `append_frame()` writes JSONL with `{direction, frame, timestamp, error?}` → no audio payload ever logged. |
| 0073 | Specify — security baseline | DONE | `docs/SECURITY_INVARIANTS_CHECKLIST.md` | a407329 | Security invariants checklist written: 12 invariants (allow-list, path jail, no shell, confirm policy, audit log, CRC validation, sequence recovery, frame size bound, retry bounds, measurement parser, simulation fails closed, virtual mode explicit). All implemented and tested. Attack surface analysis with test coverage. Human approval gates documented. |
| 0074 | Implement — security baseline | DONE | `docs/SECURITY_INVARIANTS_CHECKLIST.md` | a407329 | Checklist implemented as reference. All invariants already enforced in code (host_agent.py, launcher.py, protocol.py, audit_log.py, reliability.py, measurements.py). |
| 0075 | Test — security baseline | DONE | `make test` (7 security tests) | a407329 | All 7 security tests pass: forbid shell, measurement parser bounded, path jail, simulation fails closed, risky action requires confirm, unknown verb rejected, virtual run with open flag. |
| 0076 | Run — security baseline | DONE | `make audit`, `make sim-demo` | a407329 | Audit script validates security invariants. Sim-demo exercises full loop with allow-listed verbs only. |
| 0077 | Review — security baseline | DONE | `docs/SECURITY_INVARIANTS_CHECKLIST.md`, test logs | a407329 | Safety: 12 invariants cover all identified attack vectors. No shell execution possible. Path jail mathematically enforced (ROOT in parents). Confirm gate on destructive action. Audit log append-only. CRC on every frame. Retry bounds prevent infinite loops. Virtual mode explicitly labeled. |
| 0078 | Document — security baseline | DONE | `docs/SECURITY_INVARIANTS_CHECKLIST.md` | a407329 | Checklist documented with provenance. |
| 0079 | Integrate — security baseline | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Security baseline connected to Phase 1.9 (evidence conventions). Next step 0081 can use this output. |
| 0080 | Gate — security baseline | DONE | `docs/SECURITY_INVARIANTS_CHECKLIST.md`, `make test` pass | a407329 | Gate passed: security invariants checklist complete and all tests pass. Phase 1.8 complete. Unblocking Phase 1.9. |
| 0081 | Inspect — evidence conventions | DONE | `results/`, `docs/PHASE_A_STATUS.md`, `bench/`, `deck/out/`, `tools/provenance.py` | a407329 | Inspected evidence conventions: (1) Results directory: `results/*.json` for audit, power, pinmap, enclosure, summary, timing; `results/*.csv` for virtual trials; `results/figures/*.png` for plots. (2) Labels: SIMULATED (virtual bench), TARGET (analytical estimates), ESTIMATED (not yet used), MEASURED (requires hardware). (3) Audit log: `logs/host_agent.jsonl` JSONL with frame metadata. (4) Phase-A status matrix explicitly labels each requirement status. (5) Provenance tool: `tools/provenance.py` for evidence tracking. (6) Benchmark: `bench/run_benchmarks.py` generates `results/summary.json` with SIMULATED label. |
| 0082 | Trace — evidence conventions | DONE | `bench/run_benchmarks.py`, `bench/validate_summary.py`, `bench/analyze.py`, `tools/provenance.py` | a407329 | Traced evidence generation: (1) `make bench` → `run_benchmarks.py` generates `results/virtual_trials.csv` (30 rows, SIMULATED) → `validate_summary.py` creates `results/summary.json` with schema validation → `analyze.py` generates figures in `results/figures/`. (2) `make audit` → `audit_phase_a.py` creates `results/phase_a_audit.json` with provenance (git commit, timestamp, config). (3) `make hardware-check` → `validate_pinmap.py` creates `results/pinmap_validation.json` → `power_budget.py` creates `results/power_budget.json` (TARGET label). (4) `make cad-check` → `analytical_checks.py` creates `results/enclosure_estimate.json`. (5) All results carry explicit labels (SIMULATED, TARGET, MEASURED) per convention. |
| 0083 | Specify — evidence conventions | DONE | `docs/EVIDENCE_CONVENTIONS.md` | a407329 | Evidence conventions specified: directory structure, 4-label taxonomy (MEASURED/SIMULATED/TARGET/ESTIMATED), file naming patterns, JSON schema with provenance, audit log format (JSONL, no audio), human evidence requirements, provenance tracking, enforcement via validation tools. |
| 0084 | Implement — evidence conventions | DONE | `docs/EVIDENCE_CONVENTIONS.md` | a407329 | Conventions implemented as reference. Existing evidence generators (bench, audit, hardware-check, cad-check) already produce compliant output with provenance and labels. |
| 0085 | Test — evidence conventions | DONE | `make bench`, `make audit`, `make hardware-check`, `make cad-check` | a407329 | Verified: `results/summary.json` has provenance + SIMULATED label, `results/phase_a_audit.json` has provenance + explicit labels, `results/pinmap_validation.json` validated, `results/power_budget.json` has TARGET label, `results/enclosure_estimate.json` generated. All JSON files include provenance block. |
| 0086 | Run — evidence conventions | DONE | `make phase-a` | a407329 | Full Phase-A workflow generates all evidence artifacts with correct conventions. No unlabeled numbers in output. |
| 0087 | Review — evidence conventions | DONE | `docs/EVIDENCE_CONVENTIONS.md`, `results/*.json` | a407329 | Safety: No audio in audit logs. Honesty: All virtual results labeled SIMULATED, analytical TARGET. Completeness: Provenance on all generated files. Enforcement: validate_summary.py rejects non-compliant summaries. |
| 0088 | Document — evidence conventions | DONE | `docs/EVIDENCE_CONVENTIONS.md` | a407329 | Conventions documented with provenance. |
| 0089 | Integrate — evidence conventions | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Evidence conventions connected to Phase 1.10 (risk and schedule baseline). Next step 0091 can use this output. |
| 0090 | Gate — evidence conventions | DONE | `docs/EVIDENCE_CONVENTIONS.md`, `make phase-a` pass | a407329 | Gate passed: evidence directory and naming convention established and enforced. Phase 1.9 complete. Unblocking Phase 1.10. |
| 0091 | Inspect — risk and schedule baseline | DONE | `docs/roadmap.csv`, `docs/FMEA.csv`, `docs/FMEA_TEST_MAP.csv`, `TODO_HUMAN.md`, `docs/PHASE_A_STATUS.md` | a407329 | Inspected risk sources: (1) Firmware build blocked on ESP-IDF install (TODO_HUMAN.md Day 1). (2) Dataset collection blocked on hardware + consent (TODO_HUMAN.md Day 4). (3) ML training blocked on dataset + toolchain (Phase-A #9). (4) PCB design blocked on KiCad work + Raphael archive (Phase-A #16). (5) Integration blocked on firmware + ML + hardware (TODO_HUMAN.md Days 5-6). (6) Demonstration blocked on all above (TODO_HUMAN.md Day 6). FMEA.csv lists 20 failure modes with severity/occurrence/detection. Roadmap.csv has 14-day execution checklist. |
| 0092 | Trace — risk and schedule baseline | DONE | `docs/FMEA.csv`, `docs/FMEA_TEST_MAP.csv`, `TODO_HUMAN.md`, `docs/roadmap.csv` | a407329 | Traced risk dependencies: FMEA rows map to test cases in FMEA_TEST_MAP.csv (e.g., "comm CRC error" → test_crc_fault_recovers_sequence_and_returns_nack). Roadmap days have sequential dependencies: Day 1 (ESP-IDF) → Day 2 (I2S capture) → Day 3 (CDC echo) → Day 4 (dataset) → Day 5 (train/flash) → Day 6 (first demo). Critical path: ESP-IDF install → firmware build → hardware bring-up → dataset → ML → integration. Parallelizable: deck drafting, CAD enclosure, documentation. |
| 0093 | Specify — risk and schedule baseline | DONE | `docs/RISK_REGISTER.md` | a407329 | Risk register and milestone sequence written: 15 risks prioritized (3 Critical, 4 High, 8 Medium), 14-day execution plan with dependencies, critical path (6 days), parallel workstreams. All blockers from Phase-A status mapped to risks. |
| 0094 | Implement — risk and schedule baseline | DONE | `docs/RISK_REGISTER.md` | a407329 | Register implemented as reference. Mitigations mapped to TODO_HUMAN.md days. FMEA_TEST_MAP.csv already links risks to tests. |
| 0095 | Test — risk and schedule baseline | DONE | `make test` (FMEA tests), `tools/validate_fmea.py` | a407329 | Verified: `test_all_rows_have_evidence_mapping` passes (all 20 FMEA rows have test mapping). `validate_fmea.py` validates FMEA.csv structure. |
| 0096 | Run — risk and schedule baseline | DONE | `make audit` (includes FMEA validation) | a407329 | Audit includes FMEA validation. Risk register consistent with Phase-A blockers. |
| 0097 | Review — risk and schedule baseline | DONE | `docs/RISK_REGISTER.md`, `docs/FMEA.csv`, `docs/FMEA_TEST_MAP.csv` | a407329 | Safety: Critical risks (R1, R2, R3) have dedicated Day 1-4 actions. Honesty: Simulated evidence labeled, no MEASURED claims without hardware. Feasibility: 14-day plan has 8 days slack on critical path. |
| 0098 | Document — risk and schedule baseline | DONE | `docs/RISK_REGISTER.md` | a407329 | Register documented with provenance. |
| 0099 | Integrate — risk and schedule baseline | DONE | `docs/WORKFLOW_STATUS.md` (updated) | a407329 | Risk baseline completes Phase 1. All Phase 1 workstreams (1.1-1.10) complete or blocked with documented blockers. Ready for Phase 2. |
| 0100 | Gate — risk and schedule baseline | DONE | `docs/RISK_REGISTER.md`, `make audit` pass | a407329 | Gate passed: prioritized risk register and milestone sequence complete. Phase 1.10 complete. **PHASE 1 COMPLETE**. Unblocking Phase 2 (Host runtime and deterministic task execution). |
| 0101 | Inspect — host startup and configuration | NOT_STARTED | | | |
| 0102 | Trace — host startup and configuration | NOT_STARTED | | | |
| 0103 | Specify — host startup and configuration | NOT_STARTED | | | |
| 0104 | Implement — host startup and configuration | NOT_STARTED | | | |
| 0105 | Test — host startup and configuration | NOT_STARTED | | | |
| 0106 | Run — host startup and configuration | NOT_STARTED | | | |
| 0107 | Review — host startup and configuration | NOT_STARTED | | | |
| 0108 | Document — host startup and configuration | NOT_STARTED | | | |
| 0109 | Integrate — host startup and configuration | NOT_STARTED | | | |
| 0110 | Gate — host startup and configuration | NOT_STARTED | | | |
| 0111 | Inspect — host agent dispatcher | NOT_STARTED | | | |
| 0112 | Trace — host agent dispatcher | NOT_STARTED | | | |
| 0113 | Specify — host agent dispatcher | NOT_STARTED | | | |
| 0114 | Implement — host agent dispatcher | NOT_STARTED | | | |
| 0115 | Test — host agent dispatcher | NOT_STARTED | | | |
| 0116 | Run — host agent dispatcher | NOT_STARTED | | | |
| 0117 | Review — host agent dispatcher | NOT_STARTED | | | |
| 0118 | Document — host agent dispatcher | NOT_STARTED | | | |
| 0119 | Integrate — host agent dispatcher | NOT_STARTED | | | |
| 0120 | Gate — host agent dispatcher | NOT_STARTED | | | |
| 0121 | Inspect — session and time sync | NOT_STARTED | | | |
| 0112 | Trace — session and time sync | NOT_STARTED | | | |
| 0123 | Specify — session and time sync | NOT_STARTED | | | |
| 0124 | Implement — session and time sync | NOT_STARTED | | | |
| 0125 | Test — session and time sync | NOT_STARTED | | | |
| 0126 | Run — session and time sync | NOT_STARTED | | | |
| 0127 | Review — session and time sync | NOT_STARTED | | | |
| 0128 | Document — session and time sync | NOT_STARTED | | | |
| 0129 | Integrate — session and time sync | NOT_STARTED | | | |
| 0130 | Gate — session and time sync | NOT_STARTED | | | |
| 0131 | Inspect — launcher and allow-list | NOT_STARTED | | | |
| 0132 | Trace — launcher and allow-list | NOT_STARTED | | | |
| 0133 | Specify — launcher and allow-list | NOT_STARTED | | | |
| 0134 | Implement — launcher and allow-list | NOT_STARTED | | | |
| 0135 | Test — launcher and allow-list | NOT_STARTED | | | |
| 0136 | Run — launcher and allow-list | NOT_STARTED | | | |
| 0137 | Review — launcher and allow-list | NOT_STARTED | | | |
| 0138 | Document — launcher and allow-list | NOT_STARTED | | | |
| 0139 | Integrate — launcher and allow-list | NOT_STARTED | | | |
| 0140 | Gate — launcher and allow-list | NOT_STARTED | | | |
| 0141 | Inspect — audit log and confirmation | NOT_STARTED | | | |
| 0142 | Trace — audit log and confirmation | NOT_STARTED | | | |
| 0143 | Specify — audit log and confirmation | NOT_STARTED | | | |
| 0144 | Implement — audit log and confirmation | NOT_STARTED | | | |
| 0145 | Test — audit log and confirmation | NOT_STARTED | | | |
| 0146 | Run — audit log and confirmation | NOT_STARTED | | | |
| 0147 | Review — audit log and confirmation | NOT_STARTED | | | |
| 0148 | Document — audit log and confirmation | NOT_STARTED | | | |
| 0149 | Integrate — audit log and confirmation | NOT_STARTED | | | |
| 0150 | Gate — audit log and confirmation | NOT_STARTED | | | |
| 0151 | Inspect — virtual device transport | NOT_STARTED | | | |
| 0152 | Trace — virtual device transport | NOT_STARTED | | | |
| 0153 | Specify — virtual device transport | NOT_STARTED | | | |
| 0154 | Implement — virtual device transport | NOT_STARTED | | | |
| 0155 | Test — virtual device transport | NOT_STARTED | | | |
| 0156 | Run — virtual device transport | NOT_STARTED | | | |
| 0157 | Review — virtual device transport | NOT_STARTED | | | |
| 0158 | Document — virtual device transport | NOT_STARTED | | | |
| 0159 | Integrate — virtual device transport | NOT_STARTED | | | |
| 0160 | Gate — virtual device transport | NOT_STARTED | | | |
| 0161 | Inspect — host reliability and retries | NOT_STARTED | | | |
| 0162 | Trace — host reliability and retries | NOT_STARTED | | | |
| 0163 | Specify — host reliability and retries | NOT_STARTED | | | |
| 0164 | Implement — host reliability and retries | NOT_STARTED | | | |
| 0165 | Test — host reliability and retries | NOT_STARTED | | | |
| 0166 | Run — host reliability and retries | NOT_STARTED | | | |
| 0167 | Review — host reliability and retries | NOT_STARTED | | | |
| 0168 | Document — host reliability and retries | NOT_STARTED | | | |
| 0169 | Integrate — host reliability and retries | NOT_STARTED | | | |
| 0170 | Gate — host reliability and retries | NOT_STARTED | | | |
| 0171 | Inspect — host startup gate | NOT_STARTED | | | |
| 0172 | Trace — host startup gate | NOT_STARTED | | | |
| 0173 | Specify — host startup gate | NOT_STARTED | | | |
| 0174 | Implement — host startup gate | NOT_STARTED | | | |
| 0175 | Test — host startup gate | NOT_STARTED | | | |
| 0176 | Run — host startup gate | NOT_STARTED | | | |
| 0177 | Review — host startup gate | NOT_STARTED | | | |
| 0178 | Document — host startup gate | NOT_STARTED | | | |
| 0179 | Integrate — host startup gate | NOT_STARTED | | | |
| 0180 | Gate — host startup gate | NOT_STARTED | | | |
| 0181 | Inspect — context store Python | NOT_STARTED | | | |
| 0182 | Trace — context store Python | NOT_STARTED | | | |
| 0183 | Specify — context store Python | NOT_STARTED | | | |
| 0184 | Implement — context store Python | NOT_STARTED | | | |
| 0185 | Test — context store Python | NOT_STARTED | | | |
| 0186 | Run — context store Python | NOT_STARTED | | | |
| 0187 | Review — context store Python | NOT_STARTED | | | |
| 0188 | Document — context store Python | NOT_STARTED | | | |
| 0189 | Integrate — context store Python | NOT_STARTED | | | |
| 0190 | Gate — context store Python | NOT_STARTED | | | |
| 0191 | Inspect — context store C firmware | NOT_STARTED | | | |
| 0192 | Trace — context store C firmware | NOT_STARTED | | | |
| 0193 | Specify — context store C firmware | NOT_STARTED | | | |
| 0194 | Implement — context store C firmware | NOT_STARTED | | | |
| 0195 | Test — context store C firmware | NOT_STARTED | | | |
| 0196 | Run — context store C firmware | NOT_STARTED | | | |
| 0197 | Review — context store C firmware | NOT_STARTED | | | |
| 0198 | Document — context store C firmware | NOT_STARTED | | | |
| 0199 | Integrate — context store C firmware | NOT_STARTED | | | |
| 0200 | Gate — context store C firmware | NOT_STARTED | | | |
| 0201 | Inspect — device protocol context | NOT_STARTED | | | |
| 0202 | Trace — device protocol context | NOT_STARTED | | | |
| 0203 | Specify — device protocol context | NOT_STARTED | | | |
| 0204 | Implement — device protocol context | NOT_STARTED | | | |
| 0205 | Test — device protocol context | NOT_STARTED | | | |
| 0206 | Run — device protocol context | NOT_STARTED | | | |
| 0207 | Review — device protocol context | NOT_STARTED | | | |
| 0208 | Document — device protocol context | NOT_STARTED | | | |
| 0209 | Integrate — device protocol context | NOT_STARTED | | | |
| 0210 | Gate — device protocol context | NOT_STARTED | | | |
| 0211 | Inspect — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0212 | Trace — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0213 | Specify — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0214 | Implement — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0215 | Test — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0216 | Run — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0217 | Review — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0218 | Document — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0219 | Integrate — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0220 | Gate — LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0221 | Inspect — context recovery and bounds | NOT_STARTED | | | |
| 0222 | Trace — context recovery and bounds | NOT_STARTED | | | |
| 0223 | Specify — context recovery and bounds | NOT_STARTED | | | |
| 0224 | Implement — context recovery and bounds | NOT_STARTED | | | |
| 0225 | Test — context recovery and bounds | NOT_STARTED | | | |
| 0226 | Run — context recovery and bounds | NOT_STARTED | | | |
| 0227 | Review — context recovery and bounds | NOT_STARTED | | | |
| 0228 | Document — context recovery and bounds | NOT_STARTED | | | |
| 0229 | Integrate — context recovery and bounds | NOT_STARTED | | | |
| 0230 | Gate — context recovery and bounds | NOT_STARTED | | | |
| 0231 | Inspect — protocol encode/decode C | NOT_STARTED | | | |
| 0232 | Trace — protocol encode/decode C | NOT_STARTED | | | |
| 0233 | Specify — protocol encode/decode C | NOT_STARTED | | | |
| 0234 | Implement — protocol encode/decode C | NOT_STARTED | | | |
| 0235 | Test — protocol encode/decode C | NOT_STARTED | | | |
| 0236 | Run — protocol encode/decode C | NOT_STARTED | | | |
| 0237 | Review — protocol encode/decode C | NOT_STARTED | | | |
| 0238 | Document — protocol encode/decode C | NOT_STARTED | | | |
| 0239 | Integrate — protocol encode/decode C | NOT_STARTED | | | |
| 0240 | Gate — protocol encode/decode C | NOT_STARTED | | | |
| 0241 | Inspect — CRC16 vectors and parity | NOT_STARTED | | | |
| 0242 | Trace — CRC16 vectors and parity | NOT_STARTED | | | |
| 0243 | Specify — CRC16 vectors and parity | NOT_STARTED | | | |
| 0244 | Implement — CRC16 vectors and parity | NOT_STARTED | | | |
| 0245 | Test — CRC16 vectors and parity | NOT_STARTED | | | |
| 0246 | Run — CRC16 vectors and parity | NOT_STARTED | | | |
| 0247 | Review — CRC16 vectors and parity | NOT_STARTED | | | |
| 0248 | Document — CRC16 vectors and parity | NOT_STARTED | | | |
| 0249 | Integrate — CRC16 vectors and parity | NOT_STARTED | | | |
| 0250 | Gate — CRC16 vectors and parity | NOT_STARTED | | | |
| 0251 | Inspect — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0252 | Trace — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0253 | Specify — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0254 | Implement — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0255 | Test — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0256 | Run — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0257 | Review — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0258 | Document — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0259 | Integrate — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0260 | Gate — ACK/NACK/retry policy | NOT_STARTED | | | |
| 0261 | Inspect — fault injection and recovery | NOT_STARTED | | | |
| 0262 | Trace — fault injection and recovery | NOT_STARTED | | | |
| 0263 | Specify — fault injection and recovery | NOT_STARTED | | | |
| 0264 | Implement — fault injection and recovery | NOT_STARTED | | | |
| 0265 | Test — fault injection and recovery | NOT_STARTED | | | |
| 0266 | Run — fault injection and recovery | NOT_STARTED | | | |
| 0267 | Review — fault injection and recovery | NOT_STARTED | | | |
| 0268 | Document — fault injection and recovery | NOT_STARTED | | | |
| 0269 | Integrate — fault injection and recovery | NOT_STARTED | | | |
| 0270 | Gate — fault injection and recovery | NOT_STARTED | | | |
| 0271 | Inspect — serial transport and timeouts | NOT_STARTED | | | |
| 0272 | Trace — serial transport and timeouts | NOT_STARTED | | | |
| 0273 | Specify — serial transport and timeouts | NOT_STARTED | | | |
| 0274 | Implement — serial transport and timeouts | NOT_STARTED | | | |
| 0275 | Test — serial transport and timeouts | NOT_STARTED | | | |
| 0276 | Run — serial transport and timeouts | NOT_STARTED | | | |
| 0277 | Review — serial transport and timeouts | NOT_STARTED | | | |
| 0278 | Document — serial transport and timeouts | NOT_STARTED | | | |
| 0279 | Integrate — serial transport and timeouts | NOT_STARTED | | | |
| 0280 | Gate — serial transport and timeouts | NOT_STARTED | | | |
| 0281 | Inspect — protocol hardening gate | NOT_STARTED | | | |
| 0282 | Trace — protocol hardening gate | NOT_STARTED | | | |
| 0283 | Specify — protocol hardening gate | NOT_STARTED | | | |
| 0284 | Implement — protocol hardening gate | NOT_STARTED | | | |
| 0285 | Test — protocol hardening gate | NOT_STARTED | | | |
| 0286 | Run — protocol hardening gate | NOT_STARTED | | | |
| 0287 | Review — protocol hardening gate | NOT_STARTED | | | |
| 0288 | Document — protocol hardening gate | NOT_STARTED | | | |
| 0289 | Integrate — protocol hardening gate | NOT_STARTED | | | |
| 0290 | Gate — protocol hardening gate | NOT_STARTED | | | |
| 0291 | Inspect — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0292 | Trace — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0293 | Specify — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0294 | Implement — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0295 | Test — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0296 | Run — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0297 | Review — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0298 | Document — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0299 | Integrate — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0300 | Gate — ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0301 | Inspect — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0302 | Trace — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0303 | Specify — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0304 | Implement — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0305 | Test — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0306 | Run — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0307 | Review — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0308 | Document — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0309 | Integrate — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0310 | Gate — I2S/GDMA audio capture | NOT_STARTED | | | |
| 0311 | Inspect — MFCC feature extraction C | NOT_STARTED | | | |
| 0312 | Trace — MFCC feature extraction C | NOT_STARTED | | | |
| 0313 | Specify — MFCC feature extraction C | NOT_STARTED | | | |
| 0314 | Implement — MFCC feature extraction C | NOT_STARTED | | | |
| 0315 | Test — MFCC feature extraction C | NOT_STARTED | | | |
| 0316 | Run — MFCC feature extraction C | NOT_STARTED | | | |
| 0317 | Review — MFCC feature extraction C | NOT_STARTED | | | |
| 0318 | Document — MFCC feature extraction C | NOT_STARTED | | | |
| 0319 | Integrate — MFCC feature extraction C | NOT_STARTED | | | |
| 0320 | Gate — MFCC feature extraction C | NOT_STARTED | | | |
| 0321 | Inspect — intent classification table | NOT_STARTED | | | |
| 0322 | Trace — intent classification table | NOT_STARTED | | | |
| 0323 | Specify — intent classification table | NOT_STARTED | | | |
| 0324 | Implement — intent classification table | NOT_STARTED | | | |
| 0325 | Test — intent classification table | NOT_STARTED | | | |
| 0326 | Run — intent classification table | NOT_STARTED | | | |
| 0327 | Review — intent classification table | NOT_STARTED | | | |
| 0328 | Document — intent classification table | NOT_STARTED | | | |
| 0329 | Integrate — intent classification table | NOT_STARTED | | | |
| 0330 | Gate — intent classification table | NOT_STARTED | | | |
| 0331 | Inspect — PTT button and LED UI | NOT_STARTED | | | |
| 0332 | Trace — PTT button and LED UI | NOT_STARTED | | | |
| 0333 | Specify — PTT button and LED UI | NOT_STARTED | | | |
| 0334 | Implement — PTT button and LED UI | NOT_STARTED | | | |
| 0335 | Test — PTT button and LED UI | NOT_STARTED | | | |
| 0336 | Run — PTT button and LED UI | NOT_STARTED | | | |
| 0337 | Review — PTT button and LED UI | NOT_STARTED | | | |
| 0338 | Document — PTT button and LED UI | NOT_STARTED | | | |
| 0339 | Integrate — PTT button and LED UI | NOT_STARTED | | | |
| 0340 | Gate — PTT button and LED UI | NOT_STARTED | | | |
| 0341 | Inspect — firmware integration and build | NOT_STARTED | | | |
| 0342 | Trace — firmware integration and build | NOT_STARTED | | | |
| 0343 | Specify — firmware integration and build | NOT_STARTED | | | |
| 0344 | Implement — firmware integration and build | NOT_STARTED | | | |
| 0345 | Test — firmware integration and build | NOT_STARTED | | | |
| 0346 | Run — firmware integration and build | NOT_STARTED | | | |
| 0347 | Review — firmware integration and build | NOT_STARTED | | | |
| 0348 | Document — firmware integration and build | NOT_STARTED | | | |
| 0349 | Integrate — firmware integration and build | NOT_STARTED | | | |
| 0350 | Gate — firmware integration and build | NOT_STARTED | | | |
| 0351 | Inspect — dataset collection tool | NOT_STARTED | | | |
| 0352 | Trace — dataset collection tool | NOT_STARTED | | | |
| 0353 | Specify — dataset collection tool | NOT_STARTED | | | |
| 0354 | Implement — dataset collection tool | NOT_STARTED | | | |
| 0355 | Test — dataset collection tool | NOT_STARTED | | | |
| 0356 | Run — dataset collection tool | NOT_STARTED | | | |
| 0357 | Review — dataset collection tool | NOT_STARTED | | | |
| 0358 | Document — dataset collection tool | NOT_STARTED | | | |
| 0359 | Integrate — dataset collection tool | NOT_STARTED | | | |
| 0360 | Gate — dataset collection tool | NOT_STARTED | | | |
| 0361 | Inspect — speaker-split dataset | NOT_STARTED | | | |
| 0362 | Trace — speaker-split dataset | NOT_STARTED | | | |
| 0363 | Specify — speaker-split dataset | NOT_STARTED | | | |
| 0364 | Implement — speaker-split dataset | NOT_STARTED | | | |
| 0365 | Test — speaker-split dataset | NOT_STARTED | | | |
| 0366 | Run — speaker-split dataset | NOT_STARTED | | | |
| 0367 | Review — speaker-split dataset | NOT_STARTED | | | |
| 0368 | Document — speaker-split dataset | NOT_STARTED | | | |
| 0369 | Integrate — speaker-split dataset | NOT_STARTED | | | |
| 0370 | Gate — speaker-split dataset | NOT_STARTED | | | |
| 0371 | Inspect — DS-CNN training pipeline | NOT_STARTED | | | |
| 0372 | Trace — DS-CNN training pipeline | NOT_STARTED | | | |
| 0373 | Specify — DS-CNN training pipeline | NOT_STARTED | | | |
| 0374 | Implement — DS-CNN training pipeline | NOT_STARTED | | | |
| 0375 | Test — DS-CNN training pipeline | NOT_STARTED | | | |
| 0376 | Run — DS-CNN training pipeline | NOT_STARTED | | | |
| 0377 | Review — DS-CNN training pipeline | NOT_STARTED | | | |
| 0378 | Document — DS-CNN training pipeline | NOT_STARTED | | | |
| 0379 | Integrate — DS-CNN training pipeline | NOT_STARTED | | | |
| 0380 | Gate — DS-CNN training pipeline | NOT_STARTED | | | |
| 0381 | Inspect — int8 TFLite export | NOT_STARTED | | | |
| 0382 | Trace — int8 TFLite export | NOT_STARTED | | | |
| 0383 | Specify — int8 TFLite export | NOT_STARTED | | | |
| 0384 | Implement — int8 TFLite export | NOT_STARTED | | | |
| 0385 | Test — int8 TFLite export | NOT_STARTED | | | |
| 0386 | Run — int8 TFLite export | NOT_STARTED | | | |
| 0387 | Review — int8 TFLite export | NOT_STARTED | | | |
| 0388 | Document — int8 TFLite export | NOT_STARTED | | | |
| 0389 | Integrate — int8 TFLite export | NOT_STARTED | | | |
| 0390 | Gate — int8 TFLite export | NOT_STARTED | | | |
| 0391 | Inspect — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0392 | Trace — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0393 | Specify — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0394 | Implement — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0395 | Test — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0396 | Run — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0397 | Review — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0398 | Document — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0399 | Integrate — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0400 | Gate — leave-one-speaker-out eval | NOT_STARTED | | | |
| 0401 | Inspect — model card and metadata | NOT_STARTED | | | |
| 0402 | Trace — model card and metadata | NOT_STARTED | | | |
| 0403 | Specify — model card and metadata | NOT_STARTED | | | |
| 0404 | Implement — model card and metadata | NOT_STARTED | | | |
| 0405 | Test — model card and metadata | NOT_STARTED | | | |
| 0406 | Run — model card and metadata | NOT_STARTED | | | |
| 0407 | Review — model card and metadata | NOT_STARTED | | | |
| 0408 | Document — model card and metadata | NOT_STARTED | | | |
| 0409 | Integrate — model card and metadata | NOT_STARTED | | | |
| 0410 | Gate — model card and metadata | NOT_STARTED | | | |
| 0411 | Inspect — Raphael KiCad archive | NOT_STARTED | | | |
| 0412 | Trace — Raphael KiCad archive | NOT_STARTED | | | |
| 0413 | Specify — Raphael KiCad archive | NOT_STARTED | | | |
| 0414 | Implement — Raphael KiCad archive | NOT_STARTED | | | |
| 0415 | Test — Raphael KiCad archive | NOT_STARTED | | | |
| 0416 | Run — Raphael KiCad archive | NOT_STARTED | | | |
| 0417 | Review — Raphael KiCad archive | NOT_STARTED | | | |
| 0418 | Document — Raphael KiCad archive | NOT_STARTED | | | |
| 0419 | Integrate — Raphael KiCad archive | NOT_STARTED | | | |
| 0420 | Gate — Raphael KiCad archive | NOT_STARTED | | | |
| 0421 | Inspect — pinmap reconciliation | NOT_STARTED | | | |
| 0422 | Trace — pinmap reconciliation | NOT_STARTED | | | |
| 0423 | Specify — pinmap reconciliation | NOT_STARTED | | | |
| 0424 | Implement — pinmap reconciliation | NOT_STARTED | | | |
| 0425 | Test — pinmap reconciliation | NOT_STARTED | | | |
| 0426 | Run — pinmap reconciliation | NOT_STARTED | | | |
| 0427 | Review — pinmap reconciliation | NOT_STARTED | | | |
| 0428 | Document — pinmap reconciliation | NOT_STARTED | | | |
| 0429 | Integrate — pinmap reconciliation | NOT_STARTED | | | |
| 0430 | Gate — pinmap reconciliation | NOT_STARTED | | | |
| 0431 | Inspect — schematic and ERC | NOT_STARTED | | | |
| 0432 | Trace — schematic and ERC | NOT_STARTED | | | |
| 0433 | Specify — schematic and ERC | NOT_STARTED | | | |
| 0434 | Implement — schematic and ERC | NOT_STARTED | | | |
| 0435 | Test — schematic and ERC | NOT_STARTED | | | |
| 0436 | Run — schematic and ERC | NOT_STARTED | | | |
| 0437 | Review — schematic and ERC | NOT_STARTED | | | |
| 0438 | Document — schematic and ERC | NOT_STARTED | | | |
| 0439 | Integrate — schematic and ERC | NOT_STARTED | | | |
| 0440 | Gate — schematic and ERC | NOT_STARTED | | | |
| 0441 | Inspect — layout and DRC | NOT_STARTED | | | |
| 0442 | Trace — layout and DRC | NOT_STARTED | | | |
| 0443 | Specify — layout and DRC | NOT_STARTED | | | |
| 0444 | Implement — layout and DRC | NOT_STARTED | | | |
| 0445 | Test — layout and DRC | NOT_STARTED | | | |
| 0446 | Run — layout and DRC | NOT_STARTED | | | |
| 0447 | Review — layout and DRC | NOT_STARTED | | | |
| 0448 | Document — layout and DRC | NOT_STARTED | | | |
| 0449 | Integrate — layout and DRC | NOT_STARTED | | | |
| 0450 | Gate — layout and DRC | NOT_STARTED | | | |
| 0451 | Inspect — BOM and procurement | NOT_STARTED | | | |
| 0452 | Trace — BOM and procurement | NOT_STARTED | | | |
| 0453 | Specify — BOM and procurement | NOT_STARTED | | | |
| 0454 | Implement — BOM and procurement | NOT_STARTED | | | |
| 0455 | Test — BOM and procurement | NOT_STARTED | | | |
| 0456 | Run — BOM and procurement | NOT_STARTED | | | |
| 0457 | Review — BOM and procurement | NOT_STARTED | | | |
| 0458 | Document — BOM and procurement | NOT_STARTED | | | |
| 0459 | Integrate — BOM and procurement | NOT_STARTED | | | |
| 0460 | Gate — BOM and procurement | NOT_STARTED | | | |
| 0461 | Inspect — enclosure and mechanical | NOT_STARTED | | | |
| 0462 | Trace — enclosure and mechanical | NOT_STARTED | | | |
| 0463 | Specify — enclosure and mechanical | NOT_STARTED | | | |
| 0464 | Implement — enclosure and mechanical | NOT_STARTED | | | |
| 0465 | Test — enclosure and mechanical | NOT_STARTED | | | |
| 0466 | Run — enclosure and mechanical | NOT_STARTED | | | |
| 0467 | Review — enclosure and mechanical | NOT_STARTED | | | |
| 0468 | Document — enclosure and mechanical | NOT_STARTED | | | |
| 0469 | Integrate — enclosure and mechanical | NOT_STARTED | | | |
| 0470 | Gate — enclosure and mechanical | NOT_STARTED | | | |
| 0471 | Inspect — fabrication readiness | NOT_STARTED | | | |
| 0472 | Trace — fabrication readiness | NOT_STARTED | | | |
| 0473 | Specify — fabrication readiness | NOT_STARTED | | | |
| 0474 | Implement — fabrication readiness | NOT_STARTED | | | |
| 0475 | Test — fabrication readiness | NOT_STARTED | | | |
| 0476 | Run — fabrication readiness | NOT_STARTED | | | |
| 0477 | Review — fabrication readiness | NOT_STARTED | | | |
| 0478 | Document — fabrication readiness | NOT_STARTED | | | |
| 0479 | Integrate — fabrication readiness | NOT_STARTED | | | |
| 0480 | Gate — fabrication readiness | NOT_STARTED | | | |
| 0481 | Inspect — dashboard structure | NOT_STARTED | | | |
| 0482 | Trace — dashboard structure | NOT_STARTED | | | |
| 0483 | Specify — dashboard structure | NOT_STARTED | | | |
| 0484 | Implement — dashboard structure | NOT_STARTED | | | |
| 0485 | Test — dashboard structure | NOT_STARTED | | | |
| 0486 | Run — dashboard structure | NOT_STARTED | | | |
| 0487 | Review — dashboard structure | NOT_STARTED | | | |
| 0488 | Document — dashboard structure | NOT_STARTED | | | |
| 0489 | Integrate — dashboard structure | NOT_STARTED | | | |
| 0490 | Gate — dashboard structure | NOT_STARTED | | | |
| 0491 | Inspect — status visibility | NOT_STARTED | | | |
| 0492 | Trace — status visibility | NOT_STARTED | | | |
| 0493 | Specify — status visibility | NOT_STARTED | | | |
| 0494 | Implement — status visibility | NOT_STARTED | | | |
| 0495 | Test — status visibility | NOT_STARTED | | | |
| 0496 | Run — status visibility | NOT_STARTED | | | |
| 0497 | Review — status visibility | NOT_STARTED | | | |
| 0498 | Document — status visibility | NOT_STARTED | | | |
| 0499 | Integrate — status visibility | NOT_STARTED | | | |
| 0500 | Gate — status visibility | NOT_STARTED | | | |
| 0501 | Inspect — deck draft and QA | NOT_STARTED | | | |
| 0502 | Trace — deck draft and QA | NOT_STARTED | | | |
| 0503 | Specify — deck draft and QA | NOT_STARTED | | | |
| 0504 | Implement — deck draft and QA | NOT_STARTED | | | |
| 0505 | Test — deck draft and QA | NOT_STARTED | | | |
| 0506 | Run — deck draft and QA | NOT_STARTED | | | |
| 0507 | Review — deck draft and QA | NOT_STARTED | | | |
| 0508 | Document — deck draft and QA | NOT_STARTED | | | |
| 0509 | Integrate — deck draft and QA | NOT_STARTED | | | |
| 0510 | Gate — deck draft and QA | NOT_STARTED | | | |
| 0511 | Inspect — integrated voice-to-action | NOT_STARTED | | | |
| 0512 | Trace — integrated voice-to-action | NOT_STARTED | | | |
| 0513 | Specify — integrated voice-to-action | NOT_STARTED | | | |
| 0514 | Implement — integrated voice-to-action | NOT_STARTED | | | |
| 0515 | Test — integrated voice-to-action | NOT_STARTED | | | |
| 0516 | Run — integrated voice-to-action | NOT_STARTED | | | |
| 0517 | Review — integrated voice-to-action | NOT_STARTED | | | |
| 0518 | Document — integrated voice-to-action | NOT_STARTED | | | |
| 0519 | Integrate — integrated voice-to-action | NOT_STARTED | | | |
| 0520 | Gate — integrated voice-to-action | NOT_STARTED | | | |
| 0521 | Inspect — benchmark evidence | NOT_STARTED | | | |
| 0522 | Trace — benchmark evidence | NOT_STARTED | | | |
| 0523 | Specify — benchmark evidence | NOT_STARTED | | | |
| 0524 | Implement — benchmark evidence | NOT_STARTED | | | |
| 0525 | Test — benchmark evidence | NOT_STARTED | | | |
| 0526 | Run — benchmark evidence | NOT_STARTED | | | |
| 0527 | Review — benchmark evidence | NOT_STARTED | | | |
| 0528 | Document — benchmark evidence | NOT_STARTED | | | |
| 0529 | Integrate — benchmark evidence | NOT_STARTED | | | |
| 0530 | Gate — benchmark evidence | NOT_STARTED | | | |
| 0531 | Inspect — FMEA test matrix | NOT_STARTED | | | |
| 0532 | Trace — FMEA test matrix | NOT_STARTED | | | |
| 0533 | Specify — FMEA test matrix | NOT_STARTED | | | |
| 0534 | Implement — FMEA test matrix | NOT_STARTED | | | |
| 0535 | Test — FMEA test matrix | NOT_STARTED | | | |
| 0536 | Run — FMEA test matrix | NOT_STARTED | | | |
| 0537 | Review — FMEA test matrix | NOT_STARTED | | | |
| 0538 | Document — FMEA test matrix | NOT_STARTED | | | |
| 0539 | Integrate — FMEA test matrix | NOT_STARTED | | | |
| 0540 | Gate — FMEA test matrix | NOT_STARTED | | | |
| 0541 | Inspect — final deck and submission | NOT_STARTED | | | |
| 0542 | Trace — final deck and submission | NOT_STARTED | | | |
| 0543 | Specify — final deck and submission | NOT_STARTED | | | |
| 0544 | Implement — final deck and submission | NOT_STARTED | | | |
| 0545 | Test — final deck and submission | NOT_STARTED | | | |
| 0546 | Run — final deck and submission | NOT_STARTED | | | |
| 0547 | Review — final deck and submission | NOT_STARTED | | | |
| 0548 | Document — final deck and submission | NOT_STARTED | | | |
| 0549 | Integrate — final deck and submission | NOT_STARTED | | | |
| 0550 | Gate — final deck and submission | NOT_STARTED | | | |
| 0551 | Inspect — install and reproducibility | NOT_STARTED | | | |
| 0552 | Trace — install and reproducibility | NOT_STARTED | | | |
| 0553 | Specify — install and reproducibility | NOT_STARTED | | | |
| 0554 | Implement — install and reproducibility | NOT_STARTED | | | |
| 0555 | Test — install and reproducibility | NOT_STARTED | | | |
| 0556 | Run — install and reproducibility | NOT_STARTED | | | |
| 0557 | Review — install and reproducibility | NOT_STARTED | | | |
| 0558 | Document — install and reproducibility | NOT_STARTED | | | |
| 0559 | Integrate — install and reproducibility | NOT_STARTED | | | |
| 0560 | Gate — install and reproducibility | NOT_STARTED | | | |
| 0561 | Inspect — operational handoff docs | NOT_STARTED | | | |
| 0562 | Trace — operational handoff docs | NOT_STARTED | | | |
| 0563 | Specify — operational handoff docs | NOT_STARTED | | | |
| 0564 | Implement — operational handoff docs | NOT_STARTED | | | |
| 0565 | Test — operational handoff docs | NOT_STARTED | | | |
| 0566 | Run — operational handoff docs | NOT_STARTED | | | |
| 0567 | Review — operational handoff docs | NOT_STARTED | | | |
| 0568 | Document — operational handoff docs | NOT_STARTED | | | |
| 0569 | Integrate — operational handoff docs | NOT_STARTED | | | |
| 0570 | Gate — operational handoff docs | NOT_STARTED | | | |
| 0571 | Inspect — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0572 | Trace — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0573 | Specify — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0574 | Implement — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0575 | Test — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0576 | Run — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0577 | Review — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0578 | Document — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0579 | Integrate — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0580 | Gate — Phase 2.1 host startup and configuration | NOT_STARTED | | | |
| 0581 | Inspect — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0582 | Trace — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0583 | Specify — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0584 | Implement — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0585 | Test — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0586 | Run — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0587 | Review — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0588 | Document — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0589 | Integrate — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0590 | Gate — Phase 2.2 host agent dispatcher | NOT_STARTED | | | |
| 0591 | Inspect — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0592 | Trace — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0593 | Specify — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0594 | Implement — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0595 | Test — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0596 | Run — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0597 | Review — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0598 | Document — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0599 | Integrate — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0600 | Gate — Phase 2.3 session and time sync | NOT_STARTED | | | |
| 0601 | Inspect — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0602 | Trace — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0603 | Specify — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0604 | Implement — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0605 | Test — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0606 | Run — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0607 | Review — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0608 | Document — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0609 | Integrate — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0610 | Gate — Phase 2.4 launcher and allow-list | NOT_STARTED | | | |
| 0611 | Inspect — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0612 | Trace — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0613 | Specify — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0614 | Implement — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0615 | Test — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0616 | Run — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0617 | Review — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0618 | Document — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0619 | Integrate — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0620 | Gate — Phase 2.5 audit log and confirmation | NOT_STARTED | | | |
| 0621 | Inspect — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0622 | Trace — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0623 | Specify — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0624 | Implement — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0625 | Test — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0626 | Run — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0627 | Review — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0628 | Document — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0629 | Integrate — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0630 | Gate — Phase 2.6 virtual device transport | NOT_STARTED | | | |
| 0631 | Inspect — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0632 | Trace — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0633 | Specify — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0634 | Implement — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0635 | Test — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0636 | Run — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0637 | Review — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0638 | Document — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0639 | Integrate — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0640 | Gate — Phase 2.7 host reliability and retries | NOT_STARTED | | | |
| 0641 | Inspect — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0642 | Trace — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0643 | Specify — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0644 | Implement — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0645 | Test — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0646 | Run — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0647 | Review — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0648 | Document — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0649 | Integrate — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0650 | Gate — Phase 2.8 host startup gate | NOT_STARTED | | | |
| 0651 | Inspect — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0652 | Trace — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0653 | Specify — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0654 | Implement — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0655 | Test — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0656 | Run — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0657 | Review — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0658 | Document — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0659 | Integrate — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0660 | Gate — Phase 3.1 context store Python | NOT_STARTED | | | |
| 0661 | Inspect — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0662 | Trace — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0663 | Specify — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0664 | Implement — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0665 | Test — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0666 | Run — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0667 | Review — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0668 | Document — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0669 | Integrate — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0670 | Gate — Phase 3.2 context store C firmware | NOT_STARTED | | | |
| 0671 | Inspect — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0672 | Trace — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0673 | Specify — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0674 | Implement — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0675 | Test — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0676 | Run — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0677 | Review — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0678 | Document — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0679 | Integrate — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0680 | Gate — Phase 3.3 device protocol context | NOT_STARTED | | | |
| 0681 | Inspect — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0682 | Trace — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0683 | Specify — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0684 | Implement — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0685 | Test — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0686 | Run — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0687 | Review — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0688 | Document — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0689 | Integrate — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0690 | Gate — Phase 3.4 LAST and YESTERDAY intents | NOT_STARTED | | | |
| 0691 | Inspect — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0692 | Trace — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0693 | Specify — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0694 | Implement — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0695 | Test — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0696 | Run — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0697 | Review — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0698 | Document — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0699 | Integrate — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0700 | Gate — Phase 3.5 context recovery and bounds | NOT_STARTED | | | |
| 0701 | Inspect — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0702 | Trace — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0703 | Specify — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0704 | Implement — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0705 | Test — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0706 | Run — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0707 | Review — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0708 | Document — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0709 | Integrate — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0710 | Gate — Phase 4.1 protocol encode/decode C | NOT_STARTED | | | |
| 0711 | Inspect — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0712 | Trace — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0713 | Specify — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0714 | Implement — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0715 | Test — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0716 | Run — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0717 | Review — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0718 | Document — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0719 | Integrate — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0720 | Gate — Phase 4.2 CRC16 vectors and parity | NOT_STARTED | | | |
| 0721 | Inspect — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0722 | Trace — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0723 | Specify — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0724 | Implement — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0725 | Test — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0726 | Run — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0727 | Review — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0728 | Document — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0729 | Integrate — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0730 | Gate — Phase 4.3 ACK/NACK/retry policy | NOT_STARTED | | | |
| 0731 | Inspect — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0732 | Trace — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0733 | Specify — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0734 | Implement — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0735 | Test — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0736 | Run — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0737 | Review — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0738 | Document — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0739 | Integrate — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0740 | Gate — Phase 4.4 fault injection and recovery | NOT_STARTED | | | |
| 0741 | Inspect — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0742 | Trace — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0743 | Specify — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0744 | Implement — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0745 | Test — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0746 | Run — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0747 | Review — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0748 | Document — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0749 | Integrate — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0750 | Gate — Phase 4.5 serial transport and timeouts | NOT_STARTED | | | |
| 0751 | Inspect — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0752 | Trace — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0753 | Specify — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0754 | Implement — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0755 | Test — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0756 | Run — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0757 | Review — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0758 | Document — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0759 | Integrate — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0760 | Gate — Phase 4.6 protocol hardening gate | NOT_STARTED | | | |
| 0761 | Inspect — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0762 | Trace — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0763 | Specify — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0764 | Implement — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0765 | Test — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0766 | Run — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0767 | Review — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0768 | Document — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0769 | Integrate — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0770 | Gate — Phase 5.1 ESP-IDF scaffold and build | NOT_STARTED | | | |
| 0771 | Inspect — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0772 | Trace — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0773 | Specify — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0774 | Implement — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0775 | Test — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0776 | Run — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0777 | Review — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0778 | Document — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0779 | Integrate — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0780 | Gate — Phase 5.2 I2S/GDMA audio capture | NOT_STARTED | | | |
| 0781 | Inspect — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0782 | Trace — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0783 | Specify — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0784 | Implement — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0785 | Test — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0786 | Run — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0787 | Review — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0788 | Document — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0789 | Integrate — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0790 | Gate — Phase 5.3 MFCC feature extraction C | NOT_STARTED | | | |
| 0791 | Inspect — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0792 | Trace — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0793 | Specify — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0794 | Implement — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0795 | Test — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0796 | Run — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0797 | Review — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0798 | Document — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0799 | Integrate — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0800 | Gate — Phase 5.4 intent classification table | NOT_STARTED | | | |
| 0801 | Inspect — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0802 | Trace — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0803 | Specify — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0804 | Implement — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0805 | Test — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0806 | Run — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0807 | Review — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0808 | Document — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0809 | Integrate — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0810 | Gate — Phase 5.5 PTT button and LED UI | NOT_STARTED | | | |
| 0811 | Inspect — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0812 | Trace — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0813 | Specify — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0814 | Implement — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0815 | Test — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0816 | Run — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0817 | Review — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0818 | Document — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0819 | Integrate — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0820 | Gate — Phase 5.6 firmware integration and build | NOT_STARTED | | | |
| 0821 | Inspect — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0822 | Trace — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0823 | Specify — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0824 | Implement — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0825 | Test — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0826 | Run — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0827 | Review — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0828 | Document — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0829 | Integrate — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0830 | Gate — Phase 6.1 dataset collection tool | NOT_STARTED | | | |
| 0831 | Inspect — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0832 | Trace — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0833 | Specify — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0834 | Implement — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0835 | Test — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0836 | Run — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0837 | Review — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0838 | Document — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0839 | Integrate — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0840 | Gate — Phase 6.2 speaker-split dataset | NOT_STARTED | | | |
| 0841 | Inspect — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0842 | Trace — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0843 | Specify — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0844 | Implement — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0845 | Test — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0846 | Run — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0847 | Review — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0848 | Document — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0849 | Integrate — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0850 | Gate — Phase 6.3 DS-CNN training pipeline | NOT_STARTED | | | |
| 0851 | Inspect — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0852 | Trace — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0853 | Specify — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0854 | Implement — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0855 | Test — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0856 | Run — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0857 | Review — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0858 | Document — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0859 | Integrate — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0860 | Gate — Phase 6.4 int8 TFLite export | NOT_STARTED | | | |
| 0861 | Inspect — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0862 | Trace — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0863 | Specify — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0864 | Implement — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0865 | Test — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0866 | Run — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0867 | Review — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0868 | Document — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0869 | Integrate — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0870 | Gate — Phase 6.5 leave-one-speaker-out eval | NOT_STARTED | | | |
| 0871 | Inspect — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0872 | Trace — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0873 | Specify — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0874 | Implement — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0875 | Test — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0876 | Run — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0877 | Review — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0878 | Document — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0879 | Integrate — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0880 | Gate — Phase 6.6 model card and metadata | NOT_STARTED | | | |
| 0881 | Inspect — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0882 | Trace — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0883 | Specify — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0884 | Implement — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0885 | Test — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0886 | Run — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0887 | Review — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0888 | Document — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0889 | Integrate — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0890 | Gate — Phase 7.1 Raphael KiCad archive | NOT_STARTED | | | |
| 0891 | Inspect — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0892 | Trace — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0893 | Specify — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0894 | Implement — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0895 | Test — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0896 | Run — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0897 | Review — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0898 | Document — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0899 | Integrate — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0900 | Gate — Phase 7.2 pinmap reconciliation | NOT_STARTED | | | |
| 0901 | Inspect — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0902 | Trace — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0903 | Specify — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0904 | Implement — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0905 | Test — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0906 | Run — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0907 | Review — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0908 | Document — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0909 | Integrate — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0910 | Gate — Phase 7.3 schematic and ERC | NOT_STARTED | | | |
| 0911 | Inspect — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0912 | Trace — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0913 | Specify — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0914 | Implement — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0915 | Test — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0916 | Run — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0917 | Review — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0918 | Document — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0919 | Integrate — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0920 | Gate — Phase 7.4 layout and DRC | NOT_STARTED | | | |
| 0921 | Inspect — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0922 | Trace — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0923 | Specify — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0924 | Implement — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0925 | Test — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0926 | Run — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0927 | Review — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0928 | Document — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0929 | Integrate — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0930 | Gate — Phase 7.5 BOM and procurement | NOT_STARTED | | | |
| 0931 | Inspect — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0932 | Trace — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0933 | Specify — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0934 | Implement — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0935 | Test — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0936 | Run — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0937 | Review — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0938 | Document — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0939 | Integrate — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0940 | Gate — Phase 7.6 enclosure and mechanical | NOT_STARTED | | | |
| 0941 | Inspect — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0942 | Trace — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0943 | Specify — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0944 | Implement — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0945 | Test — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0946 | Run — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0947 | Review — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0948 | Document — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0949 | Integrate — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0950 | Gate — Phase 7.7 fabrication readiness | NOT_STARTED | | | |
| 0951 | Inspect — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0952 | Trace — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0953 | Specify — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0954 | Implement — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0955 | Test — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0956 | Run — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0957 | Review — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0958 | Document — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0959 | Integrate — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0960 | Gate — Phase 8.1 dashboard structure | NOT_STARTED | | | |
| 0961 | Inspect — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0962 | Trace — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0963 | Specify — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0964 | Implement — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0965 | Test — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0966 | Run — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0967 | Review — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0968 | Document — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0969 | Integrate — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0970 | Gate — Phase 8.2 status visibility | NOT_STARTED | | | |
| 0971 | Inspect — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0972 | Trace — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0973 | Specify — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0974 | Implement — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0975 | Test — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0976 | Run — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0977 | Review — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0978 | Document — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0979 | Integrate — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0980 | Gate — Phase 8.3 deck draft and QA | NOT_STARTED | | | |
| 0981 | Inspect — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0982 | Trace — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0983 | Specify — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0984 | Implement — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0985 | Test — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0986 | Run — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0987 | Review — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0988 | Document — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0989 | Integrate — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0990 | Gate — Phase 9.1 integrated voice-to-action | NOT_STARTED | | | |
| 0991 | Inspect — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0992 | Trace — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0993 | Specify — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0994 | Implement — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0995 | Test — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0996 | Run — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0997 | Review — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0998 | Document — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 0999 | Integrate — Phase 9.2 benchmark evidence | NOT_STARTED | | | |
| 1000 | Gate — Phase 9.2 benchmark evidence | NOT_STARTED | | | |