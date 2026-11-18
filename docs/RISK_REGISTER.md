# Prioritized Risk Register and Milestone Sequence

**Generated:** 2026-11-18T23:30:00Z
**Git Commit:** a407329
**Status:** APPROVED

---

## Risk Register (Prioritized by Impact × Likelihood)

| ID | Risk | Impact | Likelihood | Score | Mitigation | Owner | Status |
|----|------|--------|------------|-------|------------|-------|--------|
| R1 | ESP-IDF not installed / build fails | Critical | High | 9 | Day 1 dedicated; pre-verify toolchain; fallback to Docker ESP-IDF | Human | **BLOCKED** |
| R2 | Hardware procurement delayed (ESP32-S3, mic, parts) | Critical | Medium | 6 | Order Day 1; identify alternates; simulate in parallel | Human | **BLOCKED** |
| R3 | Audio dataset consent/recording fails | Critical | Medium | 6 | 3 speakers × 480 clips; backup speakers; synthetic augmentation only for smoke test | Human | **BLOCKED** |
| R4 | ML training fails to converge / accuracy too low | High | Medium | 6 | DS-CNN architecture validated; leave-one-speaker-out eval; fallback to PTT-only | ML Lead | **BLOCKED** |
| R5 | Raphael KiCad archive incompatible with pinmap | High | Medium | 6 | Reconcile before Day 12; maintain VaaniCore pinmap as authority | HW Lead | **BLOCKED** (archive missing) |
| R6 | ngspice simulation inaccurate / fails | Medium | Low | 3 | Validate against known amplifier netlist; virtual mode for demo | SW Lead | **BLOCKED** (ngspice missing) |
| R7 | PCB fabrication timeline missed | High | Medium | 6 | Day 12 ERC/DRC; Day 13 order; use JLCPCB 24h service | HW Lead | **BLOCKED** |
| R8 | Enclosure CAD not printable/fit | Medium | Medium | 4 | Parametric model; print test fit Day 12; adjust wall thickness | HW Lead | **PLANNED** |
| R9 | Deck placeholders not filled in time | Medium | High | 6 | Draft structure done; fill evidence Day 13; rehearse Day 13 | All | **IN PROGRESS** |
| R10 | Mentor sign-off delayed | Medium | Medium | 4 | Schedule review Day 13; prepare evidence packet Day 12 | PM | **PLANNED** |
| R11 | Firmware flash fails on hardware | Medium | Medium | 4 | Day 3 CDC echo test; Day 5 flash with model; verify boot log | FW Lead | **BLOCKED** |
| R12 | I2S audio capture doesn't work | High | Medium | 6 | Day 2 WAV capture test; verify GPIO pins match pinmap | FW Lead | **BLOCKED** |
| R13 | USB serial unreliable | Medium | Low | 3 | CRC16 + retry policy tested; 300ms timeout; 3 retries | FW Lead | **MITIGATED** (tested) |
| R14 | Context loss on power cycle | Low | Low | 2 | NVS persistence tested in C; 16-event history | FW Lead | **VERIFIED** (C tests) |
| R15 | Benchmark evidence rejected (simulated as measured) | Medium | High | 6 | Strict labeling enforced (SIMULATED/TARGET/MEASURED); audit checks | All | **MITIGATED** |

---

## Milestone Sequence (14-Day Execution)

| Day | Milestone | Dependencies | Exit Criteria | Risk if Missed |
|-----|-----------|--------------|---------------|----------------|
| 1 | ESP-IDF installed, parts ordered, metadata supplied | — | `idf.py build` succeeds; BOM ordered; application ID/institution/mentor/deadline in config | **R1, R2** — entire critical path blocked |
| 2 | I2S audio capture working (WAV over I2S/DMA) | Day 1 | Firmware captures 2s WAV; GPIO pins validated | **R12** — no audio input for ML |
| 3 | CDC echo + host serial smoke test | Day 1, 2 | `make sim-demo` + serial test passes; TIME_SYNC handshake | **R11, R13** — no comms path |
| 4 | Dataset recorded (3 speakers × 480 clips) | Day 2, 3 | `tools/record_dataset.py` produces labeled WAV + metadata; speaker splits valid | **R3** — no training data |
| 5 | Model trained, int8 exported, flashed | Day 4 | `ml/train.py` + `ml/export_tflite.py` → `.tflite` → flashed; device inference test passes | **R4** — no classifier |
| 6 | First physical PTT→simulation demo | Day 1-5 | Voice → intent → serial → host → ngspice → result → context → status; 3 photos + screen recording | **R6, R11, R12** — no integrated demo |
| 7 | LAST/YESTERDAY context with 20 scripted cases | Day 6 | Context tests pass on device; recovery verified | **R14** — context broken |
| 8 | VAD/wake test; choose fallback | Day 6 | False-accept report; PTT confirmed as Day-14 path | **R4** — wake word risk |
| 9 | FMEA test matrix (confirm, unplug, garbage, crash, watchdog) | Day 3, 6 | All FMEA_TEST_MAP cases exercised; no silent failures | **R13, R15** — reliability gaps |
| 10 | P1/P2/P3 dry-run + power instrument | Day 6, 7 | `make bench` with hardware; timing study CSV started | **R6, R8** — no measurements |
| 11 | N≥30 measurements per condition + timing study | Day 10 | Analysis scripts produce MEASURED summary; boxplots generated | **R6, R15** — evidence gap |
| 12 | KiCad schematic/layout + CAD enclosure; ERC/DRC | Day 1, 5 | Native `.kicad_sch`/`.kicad_pcb`; ERC/DRC logs; enclosure STL | **R5, R7, R8** — no fab files |
| 13 | Evidence photos, citations, deck metadata; rehearse | Day 6-12 | `make deck-draft` visual QA; all placeholders filled | **R9** — submission incomplete |
| 14 | Freeze, bug-fix only, mentor review, submit, tag | Day 13 | `make deck-final`; git tag; submission package ready | **R10** — missed deadline |

---

## Critical Path

```
Day 1 (ESP-IDF) → Day 2 (I2S) → Day 3 (CDC) → Day 4 (Dataset) → Day 5 (Train/Flash) → Day 6 (Demo)
```

**Total critical path: 6 days minimum.** Slack: 8 days for integration, measurement, documentation, buffer.

---

## Parallel Workstreams (Can Start Day 1)

| Workstream | Owner | Deliverable |
|------------|-------|-------------|
| Deck drafting | All | `deck/out/Vishwakarma_Stage2_VaaniCore.pptx` (structure done) |
| CAD enclosure | HW | `hardware/cad/enclosure.py` → STL |
| Documentation | All | `docs/evidence/`, `docs/references.md` |
| FMEA test development | SW | `docs/FMEA_TEST_MAP.csv` coverage |

---

## Acceptance Criteria

- Risk register prioritized with mitigations
- 14-day milestone sequence with dependencies and exit criteria
- Critical path identified
- Parallel workstreams defined
- Next step (0094) can use this output