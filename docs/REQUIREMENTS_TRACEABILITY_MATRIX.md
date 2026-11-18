# Requirements Traceability Matrix

**Generated:** 2026-11-18T22:15:00Z
**Git Commit:** a407329
**Source Documents:** `docs/PHASE_A_STATUS.md`, `docs/DECISIONS.md`, `README.md`, `workflow.md`

---

## Matrix: Requirements → Implementation Status

| # | Requirement | Source | Implementation | Evidence | Status |
|---|-------------|--------|----------------|----------|--------|
| R1 | Python/C protocol + CRC16 vectors | Phase-A #1 | `host/protocol.py`, `firmware/components/protocol/protocol.c`, `firmware/components/protocol/crc16.c`, `tests/protocol/vectors.json` | `make protocol-test` PASS | **IMPLEMENTED** |
| R2 | ACK/NACK/retry policy | Phase-A #2 | `host/session.py`, `host/reliability.py`, `tests/test_protocol.py` | `make test` (retry tests) PASS | **IMPLEMENTED** |
| R3 | Allow-list/path jail/no shell | Phase-A #3 | `host/host_agent.py` (ALLOWED/RISKY), `host/launcher.py` (fixed argv), `tests/test_security.py` | `make test` (security tests) PASS | **IMPLEMENTED** |
| R4 | Virtual intent → host action loop | Phase-A #4 | `host/tools/virtual_device.py`, `host/tools/stdio_demo.py`, `host/session.py`, `host/host_agent.py` | `make sim-demo` PASS | **IMPLEMENTED (SIMULATED)** |
| R5 | TIME_SYNC/PROJECT_EVENT lifecycle | Phase-A #5 | `host/session.py` (time_sync, connect_frames, handle), `tests/test_session.py` | `make test` (session tests) PASS | **IMPLEMENTED** |
| R6 | LAST/YESTERDAY context | Phase-A #6 | `host/session.py` (context resolution), `firmware/components/context/context.c`, `tests/test_context.py`, `tests/test_device_context.py` | `make context-test`, `make test` PASS | **IMPLEMENTED** |
| R7 | MFCC Python/C parity | Phase-A #7 | `ml/features.py`, `firmware/components/dsp/mfcc.c`, `tests/dsp_parity.c` | `make dsp-test` PASS (max error 0.0139313) | **IMPLEMENTED** |
| R8 | I2S/GDMA/RTOS firmware | Phase-A #8 | `firmware/main/main.c`, `firmware/main/audio_capture.c`, `firmware/main/pins.h`, `firmware/sdkconfig.defaults` | `firmware/README.md` - WRITTEN_NOT_BUILT | **BLOCKED** (ESP-IDF not installed) |
| R9 | TFLite-Micro int8 classifier | Phase-A #9 | `ml/model.py`, `ml/train.py`, `ml/export_tflite.py`, `ml/eval.py`, `ml/smoke_test.py` | `ml/model_card.md` - BLOCKED_INPUT/TOOLCHAIN | **BLOCKED** (no dataset, no toolchain) |
| R10 | Human audio capture tool | Phase-A #10 | `tools/record_dataset.py` | `--help` works, needs microphone + sounddevice | **TOOLING ONLY** (blocked on hardware) |
| R11 | OLED/physical buttons/LEDs | Phase-A #11 | `firmware/main/ui.c`, `firmware/main/pins.h` (GPIO defs) | Scaffold only, OLED driver absent | **PARTIAL** (blocked on hardware) |
| R12 | N≥30 benchmark harness | Phase-A #12 | `bench/run_benchmarks.py`, `results/virtual_trials.csv` (30 rows) | `make bench` - VERIFIED_SIMULATED_ONLY | **SIMULATED** |
| R13 | Real P1/P2/P3 measurements | Phase-A #13 | `bench/timing_study.csv` (template), `results/timing_study_status.json` | No hardware result files | **BLOCKED** (hardware) |
| R14 | Official-template draft deck | Phase-A #14 | `deck/build_deck.py`, `deck/out/Vishwakarma_Stage2_VaaniCore.pptx` | `make deck-draft` - VERIFIED_STRUCTURE | **IMPLEMENTED (DRAFT)** |
| R15 | Final deck | Phase-A #15 | `deck/build_deck.py --final` | Placeholders remain | **BLOCKED** (human metadata/evidence) |
| R16 | CAD/KiCad native artifacts | Phase-A #16 | `hardware/cad/analytical_checks.py`, `hardware/cad/enclosure.py`, `hardware/kicad/README.md` | Analytical estimates only | **BLOCKED** (human design work) |
| R17 | Verified citations/prices/photos/sign-offs | Phase-A #17 | `docs/references.md`, `hardware/bom.csv` (placeholders), `docs/SUBMISSION_CHECKLIST.md` | Placeholders remain | **BLOCKED** (human evidence) |
| R18 | Offline-first operation | Decision #6 | No cloud deps in core path; ML optional | Architecture review | **IMPLEMENTED** |
| R19 | ESP-IDF v5.x target | Decision #7 | `firmware/sdkconfig.defaults`, `firmware/CMakeLists.txt` | `[[HUMAN: pin after toolchain install]]` | **PLANNED** |
| R20 | PTT as Day-14 wake path | Decision #8 | `firmware/main/ui.c` (button events), `firmware/main/pins.h` (GPIO15/16) | Scaffold only | **PLANNED** |
| R21 | Draft deck via OOXML edit | Decision #9 | `deck/build_deck.py` (lxml-based) | `make deck-draft` works | **IMPLEMENTED** |
| R22 | Optional AI/cloud out of Day-14 | Decision #10 | `ml/` separate from host/firmware | Architecture review | **IMPLEMENTED** |

---

## Status Summary

| Status | Count | Requirements |
|--------|-------|--------------|
| **IMPLEMENTED** | 7 | R1, R2, R3, R5, R6, R7, R18, R21, R22 |
| **IMPLEMENTED (SIMULATED)** | 2 | R4, R12 |
| **IMPLEMENTED (DRAFT)** | 1 | R14 |
| **TOOLING ONLY** | 1 | R10 |
| **PARTIAL** | 1 | R11 |
| **PLANNED** | 2 | R19, R20 |
| **BLOCKED** | 7 | R8, R9, R13, R15, R16, R17, (R10 partial) |

---

## Blockers Requiring Human Input

| Blocker | Requirement | Human Action Needed |
|---------|-------------|---------------------|
| ESP-IDF not installed | R8 | Install ESP-IDF v5.x, run `idf.py set-target esp32s3 && idf.py build` |
| No audio dataset | R9 | Record 3-speaker consented dataset (480 clips each) |
| No hardware | R8, R10, R11, R13 | Procure ESP32-S3 boards, microphone, wire I2S/GPIO |
| No ngspice | R13 | Install ngspice for real simulation measurements |
| KiCad design incomplete | R16 | Draw schematic/layout in KiCad 8, run ERC/DRC |
| BOM prices unknown | R17 | Verify India vendor prices/lead times |
| Deck placeholders | R15 | Supply application ID, institution, mentor, deadline, citations, photos |

---

## Acceptance Criteria

- Matrix documents all Phase-A requirements with implementation status
- Blockers explicitly identified with required human actions
- Next step (0024) can use this output