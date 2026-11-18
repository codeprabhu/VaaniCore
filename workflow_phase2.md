# VaaniCore Phase II: Physical Prototype Completion — 1,500 Steps (1001–2500)

> **Purpose:** Transform the software-only VaaniCore prototype into a physically integrated, voice-driven edge-AI coprocessor that demonstrably runs on ESP32-S3 hardware with Linux host intelligence.
>
> **Context:** Phase I (steps 1–1000) established the complete software vertical slice: simulated audio pipeline, protocol, dispatcher, context, virtual device, benchmarks, and documentation. The physical ESP32-S3 firmware has never been built; no KiCad schematic/PCB exists; no real speech dataset has been recorded; no ML model has been trained; the voice-to-action chain has only been exercised in Python simulation.
>
> **Execution model:** Same as Phase I — sequential, gated steps; maintain `docs/WORKFLOW_STATUS.md`; commit coherent milestones; never fabricate hardware measurements; run independent workstreams in parallel when blocked.

---

## Phase Map

| Phase | Title | Steps | Focus |
|-------|-------|-------|-------|
| 11 | **Workflow Integrity & Technical Audit** | 1001–1100 | Fix duplicate IDs, reconcile status, establish ground truth |
| 12 | **ESP-IDF Toolchain & Firmware Build** | 1101–1200 | Install ESP-IDF v5.x, compile firmware, resolve integration errors |
| 13 | **Hardware Design Completion** | 1201–1300 | Reconcile Raphael KiCad archive, complete schematic/ERC, PCB/DRC, BOM |
| 14 | **Physical Audio Acquisition** | 1301–1400 | Wire I2S microphone, validate capture, tune GDMA/DSP pipeline |
| 15 | **Speech Dataset Collection & Validation** | 1401–1500 | Record 3-speaker consented dataset, speaker-split, quality gates |
| 16 | **Embedded ML: Training, Evaluation, Quantization** | 1501–1600 | Train DS-CNN, leave-one-speaker-out eval, int8 TFLite export |
| 17 | **Physical ESP32/Linux Integration** | 1601–1700 | Flash firmware, validate USB CDC, end-to-end voice-to-action on hardware |
| 18 | **Local LLM & Agent Runtime** | 1701–1800 | Deploy small LLM, tool registry, task planner, verification layer |
| 19 | **Desktop Automation & Tool Orchestration** | 1801–1900 | Controlled shell/GUI/file operations, approval gates, safety |
| 20 | **Persistent Contextual Memory & Task Recovery** | 1901–2000 | Vector DB, cross-session project state, LAST/YESTERDAY on host |
| 21 | **Live Monitoring Dashboard** | 2001–2100 | Real-time device/agent/execution observability |
| 22 | **Reliability, Security & Fault Injection** | 2101–2200 | Communication faults, adversarial inputs, recovery procedures |
| 23 | **Actual Performance Benchmarking** | 2201–2300 | Physical latency, throughput, power, memory measurements |
| 24 | **End-to-End Prototype Demonstration** | 2301–2400 | Rehearsed, recorded voice-to-action demo with evidence |
| 25 | **Release Engineering & Final Documentation** | 2401–2500 | Installer, runbook, final deck, handoff package |

---

## Dependency Backbone (Critical Path)

```
11 Audit
    ↓
12 ESP-IDF install → Firmware build → Flash test
    ↓
13 Raphael KiCad → Schematic/ERC → PCB/DRC → BOM → Fab files
    ↓
14 Hardware wiring → I2S capture → GDMA/DSP validation
    ↓
15 Dataset recording (3 speakers) → Validation → Speaker-split
    ↓
16 DS-CNN training → LOO eval → int8 export → Firmware integration
    ↓
17 Physical integration: Flash → USB CDC → Voice-to-action demo
    ↓ (parallelizable from here)
18 Local LLM + Agent Runtime
19 Desktop Automation
20 Persistent Memory
21 Dashboard
22 Reliability/Fault Injection
23 Physical Benchmarks
24 End-to-End Demo
25 Release
```

**Parallel workstreams (can start after Phase 11 audit):**
- Phase 13 hardware design (KiCad work)
- Phase 18 LLM research/prototyping (software only)
- Phase 19 desktop automation scaffolding
- Phase 20 persistent memory design
- Phase 21 dashboard architecture

---

## Completion Rules (Same as Phase I)

1. **Evidence required:** Every quantitative claim labeled `MEASURED` (physical hardware), `SIMULATED` (software-only), `TARGET` (design goal), or `ESTIMATED` (rough calculation).
2. **No fabrication:** Never invent dataset samples, consent, BOM prices, component availability, test results, hardware measurements, citations, photos, or sign-offs.
3. **Hardware consistency:** Pin assignments must match across KiCad, `hardware/pinmap.csv`, firmware headers, and documentation.
4. **Security invariants:** Allow-list, path jail, no-shell, confirm-gate, audit-log must hold on physical hardware.
4. **Preserve Phase I work:** Never overwrite existing working implementations; extend or wrap them.
5. **Status tracking:** Update `docs/WORKFLOW_STATUS.md` after every completed step with: step ID, status, evidence path, commit hash, blocker/next action.
6. **Regression tests:** Run `make test`, `make sim-demo`, `make audit` after any modification.
6. **Commit discipline:** Coherent milestones, descriptive messages, no squashing of evidence.

---

## Phase 11 — Workflow Integrity & Technical Audit (Steps 1001–1100)

**Objective:** Establish a single, accurate source of truth for the entire project state before any new implementation.

### Phase 11.1: Status Tracker Reconciliation (1001–1020)

| Step | Title | Acceptance |
|------|-------|------------|
| 1001 | **Inspect — Duplicate ID audit** | Enumerate all step IDs in `WORKFLOW_STATUS.md`; flag duplicates in 0901–1000 range |
| 1002 | **Trace — Duplicate origin** | Determine which entries are original Phase I vs. appended Phase 10 |
| 1003 | **Specify — Reconciliation policy** | Define: keep latest, archive old, renumber Phase 10 to 1001+ |
| 1004 | **Implement — Renumber Phase 10** | Apply policy; update `WORKFLOW_STATUS.md` with unique IDs 1001–1100 for Phase 10 |
| 1005 | **Test — ID uniqueness** | Automated check: all step IDs unique, sequential within phases |
| 1006 | **Run — Validation** | Verify no gaps, no overlaps |
| 1007 | **Review — Policy compliance** | Confirm historical evidence preserved, no status overwritten |
| 1008 | **Document — Reconciliation log** | Record decisions, mappings old→new IDs |
| 1009 | **Integrate — Clean baseline** | `WORKFLOW_STATUS.md` ready for Phase II |
| 1010 | **Gate — Reconciliation complete** | Zero duplicates, all 1000 Phase I steps accounted |

### Phase 11.2: Implementation vs. Simulation Audit (1011–1040)

| Step | Title | Acceptance |
|------|-------|------------|
| 1011 | **Inspect — Firmware build status** | Confirm: ESP-IDF not installed, `idf.py build` never run, no `.bin` artifacts |
| 1012 | **Inspect — KiCad design status** | Confirm: no `.kicad_sch`, `.kicad_pcb` in `hardware/kicad/`; Raphael archive missing |
| 1013 | **Inspect — Dataset status** | Confirm: no `dataset/` directory, no WAV files, no `metadata.jsonl` |
| 1014 | **Inspect — ML model status** | Confirm: no trained model, no `model_int8.tflite`, no eval results |
| 1015 | **Inspect — Physical integration status** | Confirm: no ESP32 hardware connected, no serial test logs, no benchmarks |
| 1016 | **Trace — Simulation boundary** | Map every `SIMULATED` label in code/evidence to its virtual implementation |
| 1017 | **Trace — Hardware boundary** | List every `[[HUMAN: ...]]` placeholder and its blocking dependency |
| 1018 | **Specify — Ground-truth matrix** | Create `docs/PHASE_II_GROUND_TRUTH.md`: column = deliverable, row = status (DONE/SIMULATED/BLOCKED/MISSING) |
| 1019 | **Implement — Ground-truth matrix** | Populate from audit; link each cell to evidence path |
| 1020 | **Test — Matrix completeness** | Every Phase I deliverable accounted; no unknowns |
| 1021 | **Run — Cross-reference** | Verify matrix matches `WORKFLOW_STATUS.md`, `PHASE_A_STATUS.md`, `TODO_HUMAN.md` |
| 1022 | **Review — Honesty check** | No `SIMULATED` claimed as `MEASURED`; no `BLOCKED` claimed as `DONE` |
| 1023 | **Document — Audit report** | `docs/PHASE_11_AUDIT_REPORT.md` with findings, gaps, risk register |
| 1024 | **Integrate — Audit baseline** | All downstream phases reference this audit |
| 1025 | **Gate — Audit complete** | Matrix published, stakeholders informed, Phase 12 unblocked |

### Phase 11.3: Dependency & Toolchain Validation (1026–1050)

| Step | Title | Acceptance |
|------|-------|------------|
| 1026 | **Inspect — ESP-IDF availability** | Check system for ESP-IDF v5.x; if absent, record exact install procedure |
| 1027 | **Inspect — KiCad 8 availability** | Check system for KiCad 8.x; verify schematic/PCB/ERC/DRC capability |
| 1028 | **Inspect — ngspice availability** | Check for ngspice ≥40; test with `projects/amplifier/amplifier.cir` |
| 1029 | **Inspect — sounddevice/PortAudio** | Check for working microphone input path |
| 1030 | **Inspect — Python ML stack** | Verify TensorFlow, TFLite, quantization tools functional |
| 1031 | **Trace — Toolchain version matrix** | Record exact versions for all critical tools |
| 1032 | **Specify — Version pinning policy** | Define exact versions for reproducibility; update `requirements-dev.txt` |
| 1033 | **Implement — Pinned dependencies** | Freeze `requirements-dev.txt`; document ESP-IDF/KiCad/ngspice versions |
| 1034 | **Test — Clean environment build** | Fresh venv + pinned deps → `make test` passes |
| 1035 | **Run — Toolchain validation script** | Automated check: all tools present, versions match pins |
| 1036 | **Review — Gap analysis** | Document any missing tools with install instructions |
| 1037 | **Document — Toolchain manifest v2** | `docs/TOOLCHAIN_MANIFEST_v2.md` with exact versions, install URLs |
| 1038 | **Integrate — Validated toolchain** | All Phase 12+ steps assume this manifest |
| 1039 | **Gate — Toolchain validated** | Clean build from scratch succeeds |

### Phase 11.4: Security & Architecture Re-verification (1040–1070)

| Step | Title | Acceptance |
|------|-------|------------|
| 1040 | **Inspect — Security invariant coverage** | Map each invariant (allow-list, path jail, no-shell, confirm, audit, CRC, retry) to test |
| 1041 | **Trace — Attack surface on hardware** | Identify new vectors: USB descriptor, firmware update, NVS corruption, side-channels |
| 1042 | **Specify — Hardware security extensions** | Define: signed firmware, NVS encryption, rate limiting, physical tamper evidence |
| 1043 | **Implement — Security test extensions** | Add tests for new vectors (where simulatable) |
| 1044 | **Test — Security regression** | `make test` + new security tests pass |
| 1044 | **Run — Security audit** | `make audit` includes new checks |
| 1045 | **Review — Threat model update** | Document residual risks, mitigations, acceptance criteria |
| 1046 | **Document — Security audit v2** | `docs/SECURITY_AUDIT_v2.md` |
| 1047 | **Integrate — Hardened baseline** | Phase 12+ inherits updated security posture |
| 1048 | **Gate — Security re-verified** | All invariants hold; new hardware vectors documented |

### Phase 11.5: Evidence & Documentation Hygiene (1071–1100)

| Step | Title | Acceptance |
|------|-------|------------|
| 1071 | **Inspect — Evidence labeling** | Scan all `results/*.json`, `results/*.csv` for correct `MEASURED/SIMULATED/TARGET/ESTIMATED` labels |
| 1072 | **Trace — Provenance gaps** | Find any evidence file missing `provenance.generated_at_utc`, `git_commit`, `label` |
| 1073 | **Specify — Evidence standard v2** | Extend `EVIDENCE_CONVENTIONS.md` with hardware measurement requirements |
| 1074 | **Implement — Label correction** | Fix any mislabeled evidence; add provenance where missing |
| 1075 | **Test — Evidence validator** | `bench/validate_summary.py` + new checks for hardware evidence |
| 1076 | **Run — Full evidence audit** | All evidence files pass validation |
| 1077 | **Review — Documentation currency** | Check `README.md`, `PHASE_A_STATUS.md`, `SUBMISSION_CHECKLIST.md` against audit |
| 1078 | **Document — Evidence hygiene report** | `docs/EVIDENCE_HYGIENE_REPORT.md` |
| 1079 | **Integrate — Clean evidence baseline** | All evidence compliant for Phase 12+ |
| 1080 | **Gate — Evidence hygiene complete** | Zero mislabels, zero missing provenance, validator passes |

---

## Phase 12 — ESP-IDF Toolchain & Firmware Build (Steps 1101–1200)

**Objective:** Produce a compilable, flashable ESP32-S3 firmware binary from the existing scaffold.

### Phase 12.1: ESP-IDF Installation & Environment (1101–1130)

| Step | Title | Acceptance |
|------|-------|------------|
| 1101 | **Inspect — ESP-IDF v5.x install options** | Compare: official installer, Docker, manual; select based on host OS |
| 1102 | **Trace — IDF_PATH dependencies** | Identify all scripts/tools requiring `IDF_PATH` and `export.sh` |
| 1103 | **Specify — Installation procedure** | Document exact commands, version pin (e.g., `release-v5.3`), verification steps |
| 1104 | **Implement — Install ESP-IDF** | Execute procedure; run `idf.py --version` → matches pin |
| 1105 | **Test — IDF environment** | `idf.py --version`, `python3 $IDF_PATH/tools/idf_tools.py list-targets` shows esp32s3 |
| 1106 | **Run — Hello world build** | `idf.py create-project test_build && cd test_build && idf.py set-target esp32s3 && idf.py build` succeeds |
| 1107 | **Review — Environment stability** | No path conflicts, Python version compatible, no missing tools |
| 1108 | **Document — ESP-IDF install log** | `docs/ESPIDF_INSTALL_LOG.md` with commands, output, version |
| 1109 | **Integrate — IDF ready for firmware** | `IDF_PATH` exported in shell profile; `export.sh` sourced |
| 1110 | **Gate — ESP-IDF installed** | Clean `idf.py build` of test project works |

### Phase 12.2: Firmware Compilation (1111–1150)

| Step | Title | Acceptance |
|------|-------|------------|
| 1111 | **Inspect — Firmware scaffold completeness** | Verify all components (protocol, dsp, context, main) have valid CMakeLists.txt |
| 1112 | **Trace — Symbol dependencies** | Map: main.c → components; component interdependencies; NVS partition requirements |
| 1113 | **Specify — Build configuration** | Verify `sdkconfig.defaults` sets: ESP32-S3, partition table, TinyUSB CDC, NVS, log level |
| 1114 | **Implement — First firmware build** | `cd firmware && idf.py set-target esp32s3 && idf.py build` |
| 1115 | **Test — Build error resolution** | Iteratively fix: missing includes, undefined symbols, CMake errors, SDK version mismatches |
| 1116 | **Run — Successful build** | `idf.py build` completes → `build/vaanicore.bin`, `bootloader.bin`, `partition-table.bin` |
| 1117 | **Review — Binary size analysis** | Report: firmware size, free flash, RAM usage; verify fits ESP32-S3 (4MB flash, 512KB SRAM) |
| 1118 | **Document — Build log & artifacts** | `docs/FIRMWARE_BUILD_LOG.md` with commands, output, size report |
| 1119 | **Integrate — Build in CI** | Add `firmware_build` target to Makefile; document local build procedure |
| 1120 | **Gate — Firmware compiles** | Clean build from scratch produces valid `.bin` files |

### Phase 12.3: Flash & Smoke Test (1121–1160)

| Step | Title | Acceptance |
|------|-------|------------|
| 1121 | **Inspect — Hardware availability** | Confirm: ESP32-S3 dev board, USB-C cable, host USB port permissions (`dialout` group) |
| 1122 | **Trace — Flash procedure** | Document: `idf.py -p PORT flash monitor`, baud rates, bootloader offsets |
| 1123 | **Specify — Smoke test criteria** | Boot log shows: FreeRTOS start, task creation, I2S init, USB CDC enumeration, `VaaniCore scaffold` log |
| 1124 | **Implement — First flash** | `idf.py -p /dev/ttyUSB0 flash monitor` (or detected port) |
| 1125 | **Test — Boot log capture** | Save full serial output; verify all 8 tasks created, no Guru Meditation / watchdog reset |
| 1126 | **Run — CDC enumeration test** | Host `lsusb` / `dmesg` shows TinyUSB CDC device; `/dev/ttyACM*` or `/dev/ttyUSB*` appears |
| 1127 | **Review — Power/thermal check** | Board temperature reasonable; no brownout; current draw within spec |
| 1128 | **Document — Flash & boot log** | `docs/FIRST_FLASH_LOG.md` with full transcript, photos |
| 1129 | **Integrate — Flash procedure in Makefile** | `make flash` target; `make monitor` target |
| 1130 | **Gate — Firmware runs on hardware** | Board boots, enumerates CDC, prints scaffold log, no crashes |

### Phase 12.4: Component Integration Testing on Hardware (1131–1170)

| Step | Title | Acceptance |
|------|-------|------------|
| 1131 | **Inspect — Component test plan** | Define per-component hardware tests: I2S capture, MFCC, NVS, USB CDC, buttons, LEDs |
| 1132 | **Trace — Test dependencies** | Order: I2S → MFCC → intent → USB CDC → buttons/LEDs → NVS → full pipeline |
| 1133 | **Specify — Test harness** | Add `make hw-test-*` targets; each produces JSON evidence with `MEASURED` label |
| 1134 | **Implement — I2S/GDMA hardware test** | Capture 2s WAV via I2S; save to host; verify sample rate, format, no overruns |
| 1135 | **Implement — MFCC hardware test** | Feed known tone → capture MFCC → compare to Python reference (tolerance ≤0.05) |
| 1136 | **Implement — NVS persistence test** | Write context → power cycle → read back → verify 16-event history intact |
| 1137 | **Implement — USB CDC loopback test** | Host sends frames → device echoes → verify CRC, sequencing, latency |
| 1138 | **Implement — Button/LED test** | Press confirm/abort → verify ISR → queue → LED patterns (listen/busy/err) |
| 1139 | **Test — Component test execution** | Run each `make hw-test-*`; capture `MEASURED` evidence |
| 1140 | **Run — Full component suite** | All component tests pass; evidence in `results/hw_test_*.json` |
| 1141 | **Review — Integration readiness** | All components individually verified; ready for pipeline integration |
| 1142 | **Document — Hardware test reports** | `docs/HW_TEST_*.md` per component |
| 1143 | **Integrate — Component tests in CI** | Makefile targets; documented procedure |
| 1144 | **Gate — Components verified on hardware** | All component tests pass with `MEASURED` evidence |

### Phase 12.5: Pipeline Integration & Optimization (1145–1200)

| Step | Title | Acceptance |
|------|-------|------------|
| 1145 | **Inspect — Pipeline data flow** | Trace: I2S (256 frames) → GDMA → audio_task → dsp_task (MFCC) → infer_task → intent_task → comms_task |
| 1146 | **Trace — Queue sizing & latency** | Measure queue depths, task periods, end-to-end latency (PTT press → USB frame) |
| 1147 | **Specify — Integration targets** | End-to-end latency < 500ms; zero frame drops; CPU < 70% on core 0/1 |
| 1148 | **Implement — Pipeline integration** | Connect all tasks via FreeRTOS queues; enable infer_task with placeholder classifier |
| 1149 | **Test — Pipeline latency measurement** | GPIO toggle on PTT press → GPIO toggle on USB TX → oscilloscope measurement |
| 1150 | **Run — Pipeline stress test** | 5 min continuous PTT cycles; verify no queue overflows, memory leaks, watchdog resets |
| 1151 | **Review — Resource utilization** | Report: CPU per core, heap high-water, stack high-water, flash usage |
| 1152 | **Document — Pipeline integration report** | `docs/PIPELINE_INTEGRATION_REPORT.md` with latency, resource, stability data |
| 1153 | **Integrate — Full pipeline on hardware** | `make hw-pipeline-test` target produces end-to-end `MEASURED` evidence |
| 1154 | **Gate — Firmware pipeline operational** | End-to-end latency measured, stable, within targets |

---

## Phase 13 — Hardware Design Completion (Steps 1201–1300)

**Objective:** Produce fabrication-ready KiCad schematic, PCB, BOM, and enclosure from the Raphael archive or fresh design.

### Phase 13.1: Raphael Archive Reconciliation (1201–1240)

| Step | Title | Acceptance |
|------|-------|------------|
| 1201 | **Inspect — Raphael archive acquisition** | Obtain `.kicad_pro`, `.kicad_sch`, `.kicad_pcb` from source; verify KiCad 8 compatibility |
| 1202 | **Trace — Archive provenance** | Record: source, date, author, version, any known issues |
| 1203 | **Specify — Reconciliation criteria** | Pinmap match, component selection, power budget, form factor, fabrication constraints |
| 1204 | **Implement — Schematic import & review** | Open in KiCad 8; run ERC; document all violations |
| 1205 | **Implement — PCB import & review** | Open in KiCad 8; run DRC; document all violations |
| 1206 | **Trace — Pinmap comparison** | Netlist export → compare every net against `hardware/pinmap.csv` |
| 1207 | **Test — Pinmap compliance** | Automated check: every GPIO in schematic matches `pinmap.csv` exactly |
| 1208 | **Run — Conflict resolution** | For each mismatch: document, decide (adapt Raphael / fix pinmap / reject Raphael), record decision |
| 1209 | **Review — Reconciliation report** | `docs/RAPHAEL_RECONCILIATION_REPORT.md` with net-by-net comparison, decisions |
| 1210 | **Gate — Pinmap reconciled** | Zero unresolved conflicts; `pinmap.csv` authoritative; schematic/PCB compliant |

### Phase 13.2: Schematic Completion & ERC (1211–1250)

| Step | Title | Acceptance |
|------|-------|------------|
| 1211 | **Inspect — Schematic completeness** | Check: all components placed, nets labeled, power flags, no floating pins |
| 1212 | **Trace — Net naming convention** | Standardize: `NET_<FUNCTION>`, hierarchical labels consistent |
| 1213 | **Specify — ERC ruleset** | Define: severity levels, allowed warnings, zero errors policy |
| 1214 | **Implement — ERC cleanup** | Fix all ERC errors; resolve warnings or document acceptable ones |
| 1215 | **Test — ERC clean** | KiCad ERC → zero errors; warnings documented and accepted |
| 1216 | **Run — Netlist export** | Export IPC-D-356 / KiCad netlist for PCB cross-check |
| 1217 | **Review — Schematic review checklist** | `docs/SCHEMATIC_REVIEW.md`: power, decoupling, reset, clock, USB, I2S, I2C, GPIO |
| 1218 | **Document — Schematic PDF + source** | Export PDF; commit `.kicad_sch` |
| 1219 | **Integrate — Schematic in repo** | `hardware/kicad/vaanicore.kicad_sch` |
| 1220 | **Gate — Schematic ERC clean** | KiCad ERC passes; netlist matches `pinmap.csv`; PDF archived |

### Phase 13.3: PCB Layout & DRC (1221–1260)

| Step | Title | Acceptance |
|------|-------|------------|
| 1221 | **Inspect — PCB stackup & constraints** | Define: 2/4 layer, impedance targets, min trace/space, via sizes, board outline |
| 1222 | **Trace — Placement strategy** | Group: MCU central, RF keepout, power near USB, crystals close, connectors at edge |
| 1223 | **Specify — DRC ruleset** | IPC Class 2; min trace 0.15mm, space 0.15mm, via 0.3/0.6mm, copper pour rules |
| 1224 | **Implement — Component placement** | Place all footprints; 3D check for mechanical clearance |
| 1225 | **Implement — Routing** | Prioritize: USB D+/D- (90Ω diff), I2S clock, power planes, ground stitching |
| 1226 | **Implement — DRC cleanup** | Iterate until zero DRC errors; document any approved waivers |
| 1227 | **Test — DRC clean** | KiCad DRC → zero errors |
| 1228 | **Run — Signal integrity check** | USB diff pair length match < 0.5mm; I2S clock skew < 100ps |
| 1229 | **Review — PCB review checklist** | `docs/PCB_REVIEW.md`: power, ground, USB, RF, thermal, mechanical, test points |
| 1230 | **Document — PCB outputs** | Gerbers (RS-274X), drill files, pick-and-place, BOM, 3D STEP, PDF |
| 1231 | **Integrate — PCB in repo** | `hardware/kicad/vaanicore.kicad_pcb` + `hardware/kicad/fab/` |
| 1232 | **Gate — PCB DRC clean** | Zero DRC errors; Gerbers generated; ready for fab quote |

### Phase 13.4: BOM Verification & Enclosure Integration (1233–1280)

| Step | Title | Acceptance |
|------|-------|------------|
| 1233 | **Inspect — BOM completeness** | KiCad BOM export → all components have: MPN, manufacturer, qty, footprint, lifecycle status |
| 1234 | **Trace — Procurement validation** | For each line: check DigiKey/Mouser/LCSC/Indian distributors for stock, price, lead time |
| 1235 | **Specify — BOM finalization** | Resolve: DNI parts, alternates, lifecycle risks, cost targets |
| 1236 | **Implement — BOM finalization** | Update `hardware/bom.csv` with verified data; lock versions |
| 1237 | **Test — BOM cost rollup** | Total BOM cost calculated; compare to budget |
| 1238 | **Run — Enclosure-PCB fit check** | Import PCB STEP + enclosure STEP into FreeCAD/OnShape; verify clearance, mounting holes, USB/mic cutouts |
| 1239 | **Review — Mechanical integration** | `docs/MECHANICAL_INTEGRATION.md`: PCB mounting, button alignment, LED visibility, antenna keepout |
| 1240 | **Document — Fabrication package** | `hardware/kicad/fab/`: Gerbers, drill, BOM, CPL, stackup PDF, assembly drawings |
| 1241 | **Integrate — Fab package in repo** | Ready for JLCPCB/PCBWay/OSH Park upload |
| 1242 | **Gate — Fabrication ready** | ERC/DRC clean, BOM verified, enclosure fits, fab package complete |

### Phase 13.5: Fabrication & Assembly (1243–1280)

| Step | Title | Acceptance |
|------|-------|------------|
| 1243 | **Inspect — Fab house selection** | Compare: JLCPCB, PCBWay, OSH Park, Indian fabs; lead time, cost, min order |
| 1244 | **Trace — Assembly options** | Self-assemble vs. turnkey; stencil; component sourcing |
| 1245 | **Specify — Fab order** | Define: quantity (5-10), stackup, surface finish, panelization, test requirements |
| 1246 | **Implement — Place fab order** | Upload Gerbers; confirm DRC pass at fab house; pay; record order number |
| 1247 | **Test — Fab tracking** | Monitor production; document timeline |
| 1248 | **Run — Receive PCBs** | Visual inspection: soldermask, silkscreen, drill registration, edge cuts |
| 1249 | **Review — PCB quality report** | `docs/PCB_RECEIPT_REPORT.md` with photos, measurements |
| 1250 | **Document — Component kit** | Order components per BOM; verify received against BOM |
| 1251 | **Integrate — Assembly preparation** | Stencil, solder paste, pick-and-place data ready |
| 1252 | **Gate — PCBs received & verified** | Boards pass visual inspection; components kitted; ready for assembly |

### Phase 13.6: Board Bring-up (1253–1280)

| Step | Title | Acceptance |
|------|-------|------------|
| 1253 | **Inspect — Assembly plan** | Define: stencil alignment, reflow profile, hand-solder order, inspection points |
| 1254 | **Trace — Power-on sequence** | Define: visual inspection → resistance checks → 3.3V rail → MCU power → LED blink |
| 1255 | **Specify — Bring-up test points** | Define: TP_3V3, TP_VBUS, TP_XTAL, TP_I2S_*, TP_USB_*, TP_BTN_*, TP_LED_* |
| 1256 | **Implement — First power-on** | Current-limited supply; measure rails; verify no shorts |
| 1257 | **Test — MCU boot** | Flash firmware; verify boot log; USB CDC enumeration |
| 1258 | **Run — Peripheral validation** | Test each: I2S mic, buttons, LEDs, I2C OLED, USB CDC, NVS |
| 1259 | **Review — Bring-up report** | `docs/BOARD_BRINGUP_REPORT.md` with measurements, photos, issues |
| 1260 | **Document — Verified hardware** | `docs/VERIFIED_HARDWARE.md` |
| 1261 | **Integrate — Hardware baseline** | All subsequent phases use this verified hardware |
| 1262 | **Gate — Custom hardware operational** | Custom PCB boots, runs firmware, all peripherals functional |

---

## Phase 14 — Physical Audio Acquisition (Steps 1301–1400)

**Objective:** Validate the complete I2S microphone pipeline on physical hardware with measured performance.

### Phase 14.1: Microphone Hardware Integration (1301–1340)

| Step | Title | Acceptance |
|------|-------|------------|
| 1301 | **Inspect — Microphone selection** | Choose: I2S MEMS mic (e.g., ICS-43434, SPH0645); verify: 16-48kHz, 24-bit, I2S standard mode |
| 1302 | **Trace — Schematic integration** | Verify: mic VDD/GND/SCLK/WS/SD connected to ESP32-S3 GPIOs per `pinmap.csv` |
| 1303 | **Specify — Mic wiring** | Document: wire gauge, length, shielding, decoupling caps, pull resistors |
| 1304 | **Implement — Mic soldering** | Solder mic to PCB/test board; verify continuity, no shorts |
| 1305 | **Test — Mic power & clock** | Scope: VDD stable, SCLK/WS/SD toggling at 16kHz/32kHz/64kHz |
| 1306 | **Run — First audio capture** | Firmware I2S capture → save WAV to host → verify 16kHz, mono, 16-bit |
| 1307 | **Review — Signal quality** | FFT: SNR > 60dB, THD < 1%, no 50/60Hz hum, no clipping at normal speech |
| 1308 | **Document — Mic integration report** | `docs/MIC_INTEGRATION_REPORT.md` with scope captures, WAV samples |
| 1309 | **Integrate — Mic in pipeline** | Firmware I2S task produces frames for DSP task |
| 1310 | **Gate — Microphone operational** | Clean 16kHz capture, measurable SNR, no hardware issues |

### Phase 14.2: I2S/GDMA Pipeline Validation (1311–1350)

| Step | Title | Acceptance |
|------|-------|------------|
| 1311 | **Inspect — GDMA descriptor config** | Verify: 6 descriptors × 256 frames, circular, ping-pong, ISR → task notify |
| 1312 | **Trace — Buffer latency** | Measure: sample → GDMA → ISR → task notify → audio_task → queue → dsp_task |
| 1313 | **Specify — Latency targets** | End-to-end capture latency < 20ms; zero overruns/underruns in 1 hour |
| 1314 | **Implement — Overrun/underrun detection** | Firmware counters; LED error pattern on buffer error |
| 1315 | **Test — Continuous capture** | 1 hour continuous PTT cycles; log buffer errors, latency percentiles |
| 1316 | **Run — Stress test** | Max PTT frequency (press/release 5Hz); verify no frame drops |
| 1317 | **Review — GDMA performance** | Report: latency distribution, buffer utilization, error counts |
| 1318 | **Document — GDMA validation** | `docs/GDMA_VALIDATION_REPORT.md` with scope captures, latency histograms |
| 1319 | **Integrate — GDMA in pipeline** | Verified GDMA feeds DSP task reliably |
| 1320 | **Gate — GDMA pipeline validated** | Zero buffer errors in 1h; latency < 20ms p99 |

### Phase 14.3: DSP Pipeline Hardware Validation (1321–1360)

| Step | Title | Acceptance |
|------|-------|------------|
| 1321 | **Inspect — MFCC hardware vs. Python** | Feed calibrated tone (1kHz, -20dBFS) → capture → compare MFCC to Python reference |
| 1322 | **Trace — Fixed-point accuracy** | Verify: 32→16 bit saturation, DC block, pre-emphasis, FFT, mel, log, DCT all match |
| 1323 | **Specify — Accuracy tolerance** | Max abs error ≤ 0.05 vs. Python golden vector (same as Phase I sim) |
| 1324 | **Implement — Hardware MFCC test harness** | Firmware: tone gen → I2S loopback → MFCC → USB log → host comparison script |
| 1325 | **Test — MFCC parity** | Run 100 random noise captures; compute max abs error vs. Python |
| 1326 | **Run — DSP timing** | Measure: MFCC compute time per frame (target < 5ms on ESP32-S3) |
| 1327 | **Review — DSP hardware report** | `docs/DSP_HARDWARE_REPORT.md`: accuracy, timing, resource usage |
| 1328 | **Document — DSP hardware validation** | `results/dsp_hardware_parity.json` with `MEASURED` label |
| 1329 | **Integrate — DSP in pipeline** | Verified MFCC feeds intent classifier |
| 1330 | **Gate — DSP hardware validated** | Accuracy within tolerance; timing within budget; `MEASURED` evidence |

### Phase 14.4: VAD & PTT Integration (1331–1370)

| Step | Title | Acceptance |
|------|-------|------------|
| 1331 | **Inspect — VAD options** | Evaluate: energy-based, spectral flux, MFCC-based; select for ESP32-S3 constraints |
| 1332 | **Trace — PTT + VAD hybrid** | PTT = primary trigger; VAD = optional timeout/endpoint detection |
| 1333 | **Specify — VAD thresholds** | Energy floor, speech onset/offset hysteresis, min/max utterance duration |
| 1334 | **Implement — VAD in dsp_task** | Frame-level VAD decision; outputs speech/silence flag to infer_task |
| 1335 | **Test — VAD accuracy** | Record 50 utterances + 50 silence segments; compute precision/recall |
| 1336 | **Run — PTT + VAD integration** | Press PTT → capture starts → VAD detects speech end → capture stops → classify |
| 1337 | **Review — VAD/PTT report** | `docs/VAD_PTT_REPORT.md`: thresholds, precision/recall, latency |
| 1338 | **Document — VAD config** | `firmware/main/vad_config.h` with tuned thresholds |
| 1339 | **Integrate — VAD in pipeline** | VAD output gates inference; reduces compute on silence |
| 1340 | **Gate — VAD + PTT operational** | VAD precision > 95%, recall > 90%; no false triggers in quiet room |

### Phase 14.5: Audio Pipeline End-to-End (1341–1400)

| Step | Title | Acceptance |
|------|-------|------------|
| 1341 | **Inspect — Full audio chain** | Mic → I2S → GDMA → audio_task → dsp_task (MFCC+VAD) → infer_task → intent_task |
| 1342 | **Trace — End-to-end latency** | PTT press → audio capture → MFCC → inference → intent → USB frame → host ACK |
| 1343 | **Specify — E2E targets** | Latency < 500ms p99; CPU < 70%; zero frame drops in 10 min continuous |
| 1344 | **Implement — E2E test harness** | GPIO toggle on PTT → GPIO toggle on USB TX → oscilloscope + host timestamp |
| 1345 | **Test — E2E measurement** | 100 PTT cycles; record latency distribution |
| 1345 | **Run — Continuous operation** | 10 min simulated usage (random PTT intervals); monitor CPU, heap, queue depths |
| 1346 | **Review — Audio pipeline E2E report** | `docs/AUDIO_PIPELINE_E2E_REPORT.md` with latency, CPU, stability data |
| 1347 | **Document — Audio pipeline evidence** | `results/audio_pipeline_e2e.json` with `MEASURED` label |
| 1348 | **Integrate — Audio pipeline complete** | Ready for classifier integration |
| 1349 | **Gate — Physical audio pipeline operational** | All E2E targets met; `MEASURED` evidence archived |

---

## Phase 15 — Speech Dataset Collection & Validation (Steps 1401–1500)

**Objective:** Collect, validate, and prepare a real, consented, speaker-isolated dataset for DS-CNN training.

### Phase 15.1: Consent & Ethics (1401–1420)

| Step | Title | Acceptance |
|------|-------|------------|
| 1401 | **Inspect — Ethics requirements** | Define: informed consent form, data usage statement, withdrawal right, anonymization |
| 1402 | **Trace — Legal compliance** | Check: GDPR (if applicable), institutional IRB, local regulations |
| 1403 | **Specify — Consent process** | Document: verbal + written consent, witness, secure storage, retention period |
| 1404 | **Implement — Consent forms** | Create: PDF consent form, metadata sheet per speaker |
| 1405 | **Test — Consent workflow** | Dry-run with team member; verify all fields captured |
| 1406 | **Run — Collect consents** | 3 speakers sign; forms stored securely (encrypted) |
| 1407 | **Review — Consent audit** | `docs/CONSENT_AUDIT.md`: all forms present, complete, properly stored |
| 1408 | **Document — Consent records** | `docs/consent/` (encrypted) with metadata index |
| 1409 | **Integrate — Consent in dataset tool** | `tools/record_dataset.py` requires `--consent-file` per speaker |
| 1410 | **Gate — Consent complete** | 3 signed forms; metadata index; tool enforces consent |

### Phase 15.2: Recording Procedure & Environment (1411–1440)

| Step | Title | Acceptance |
|------|-------|------------|
| 1411 | **Inspect — Recording environment** | Define: quiet room (< 40dB SPL), mic position (20cm), pop filter, acoustic treatment |
| 1412 | **Trace — Recording session design** | 13 classes × 40 utterances = 520 clips/speaker; session length ~45 min |
| 1413 | **Specify — Prompt script** | Create: randomized phrase list per class; neutral carrier phrases; rest periods |
| 1414 | **Implement — Recording session script** | `tools/record_session.py`: guides speaker, plays prompts, auto-saves WAV + metadata |
| 1415 | **Test — Session dry-run** | Team member completes full session; verify WAV quality, metadata completeness |
| 1416 | **Run — Speaker 1 recording** | Execute session; monitor levels; save WAV + metadata.jsonl |
| 1417 | **Run — Speaker 2 recording** | Same procedure |
| 1418 | **Run — Speaker 3 recording** | Same procedure |
| 1419 | **Review — Session quality** | Spot-check 10% of clips: SNR, clipping, background noise, correct labeling |
| 1420 | **Gate — Sessions complete** | 3 speakers × ≥480 clips = ≥1440 WAVs; all metadata present |

### Phase 15.3: Dataset Validation & Quality Gates (1421–1460)

| Step | Title | Acceptance |
|------|-------|------------|
| 1421 | **Inspect — Dataset structure** | Verify: `dataset/<class>/<speaker>_<idx>.wav` + `metadata.jsonl` |
| 1422 | **Trace — Metadata completeness** | Every WAV has: class, filepath, duration, sample_rate, speaker_id, timestamp, consent_ref |
| 1423 | **Specify — Quality thresholds** | Duration 1.8–2.2s, RMS -20 to -6 dBFS, no clipping, SNR > 30dB |
| 1424 | **Implement — Automated QC** | `tools/validate_dataset.py`: checks all thresholds; outputs pass/fail per clip |
| 1425 | **Test — QC execution** | Run on full dataset; report pass rate, list failures |
| 1426 | **Run — Full QC pass** | Re-record any failed clips; iterate until 100% pass |
| 1427 | **Review — Dataset QC report** | `docs/DATASET_QC_REPORT.md`: pass rate, failure analysis, re-record count |
| 1428 | **Document — Final dataset manifest** | `docs/DATASET_MANIFEST.md`: total clips, per-speaker/class counts, durations |
| 1429 | **Integrate — Dataset in pipeline** | `ml/dataset.py` loads validated dataset; `ml/features.py` extracts MFCC |
| 1430 | **Gate — Dataset validated** | 100% clips pass QC; metadata complete; speaker-split ready |

### Phase 15.4: Speaker-Split Validation (1431–1470)

| Step | Title | Acceptance |
|------|-------|------------|
| 1431 | **Inspect — Split implementation** | Verify `ml/dataset.py` splits by `speaker_id`, not by sample |
| 1432 | **Trace — Split ratios** | 70/15/15 (train/val/test) per speaker; no speaker in multiple splits |
| 1433 | **Specify — Split validation** | Automated check: zero speaker overlap across splits |
| 1434 | **Implement — Split validator** | `tools/validate_split.py`: asserts no speaker_id in multiple splits |
| 1435 | **Test — Split validation** | Run on dataset; zero violations |
| 1436 | **Run — Leave-one-speaker-out folds** | Generate 3 fold manifests: (train_speakers, test_speaker) |
| 1437 | **Review — Split audit** | `docs/SPEAKER_SPLIT_AUDIT.md`: fold composition, class balance per fold |
| 1438 | **Document — Fold manifests** | `dataset/folds/fold_{1,2,3}.json` with train/val/test file lists |
| 1439 | **Integrate — Folds in training** | `ml/train.py` loads fold manifests for LOO CV |
| 1440 | **Gate — Speaker-split verified** | Zero leakage; balanced folds; manifests ready for training |

### Phase 15.5: Dataset Documentation & Release (1441–1480)

| Step | Title | Acceptance |
|------|-------|------------|
| 1441 | **Inspect — Dataset card** | Create: `docs/DATASET_CARD.md` per Google Dataset Card standard |
| 1442 | **Trace — Bias & limitations** | Document: 3 speakers only, English only, quiet room, specific mic, accent coverage |
| 1443 | **Specify — Dataset versioning** | Semantic version (v1.0.0); changelog; DOI if published |
| 1444 | **Implement — Dataset package** | `dataset/` with: WAVs, metadata.jsonl, folds/, DATASET_CARD.md, LICENSE |
| 1445 | **Test — Package integrity** | Verify: all files present, checksums match, no PII in metadata |
| 1446 | **Run — Package validation** | `tools/validate_dataset_package.py` passes |
| 1447 | **Review — Dataset card review** | Peer review: completeness, honesty, limitations clearly stated |
| 1448 | **Document — Dataset release** | `docs/DATASET_RELEASE.md` with version, date, access info |
| 1449 | **Integrate — Dataset in ML pipeline** | `ml/train.py` loads from package path |
| 1450 | **Gate — Dataset release ready** | Package complete, validated, documented, bias/limitations disclosed |

---

## Phase 16 — Embedded ML: Training, Evaluation, Quantization (Steps 1501–1600)

**Objective:** Train, evaluate, and deploy a quantized DS-CNN intent classifier on the ESP32-S3.

### Phase 16.1: Training Infrastructure (1501–1540)

| Step | Title | Acceptance |
|------|-------|------------|
| 1501 | **Inspect — Training environment** | Verify: GPU (CUDA), TensorFlow 2.x, TFLite, quantization tools, sufficient VRAM |
| 1502 | **Trace — Training config** | Review `ml/configs/default.json`: architecture, hyperparameters, data augmentation |
| 1503 | **Specify — Training procedure** | Document: seed, batch size, epochs, optimizer, LR schedule, early stopping, checkpointing |
| 1504 | **Implement — Reproducible training script** | `ml/train.py`: deterministic (seeds), resumable, logs to TensorBoard, saves best model |
| 1505 | **Test — Training dry-run** | 1 epoch on fold 1; verify: loss decreases, metrics logged, checkpoint saved |
| 1506 | **Run — Full leave-one-speaker-out training** | 3 folds × 50 epochs; total ~2.5 hours on GPU |
| 1507 | **Review — Training curves** | TensorBoard: train/val loss, accuracy, F1; no divergence, proper early stopping |
| 1508 | **Document — Training log** | `docs/TRAINING_LOG.md`: per-fold epochs, best val metrics, final test metrics |
| 1509 | **Integrate — Checkpoints in pipeline** | Best model per fold saved; int8 export uses best val loss checkpoint |
| 1510 | **Gate — Training complete** | 3 models trained; checkpoints saved; curves archived |

### Phase 16.2: Leave-One-Speaker-Out Evaluation (1511–1550)

| Step | Title | Acceptance |
|------|-------|------------|
| 1511 | **Inspect — Eval implementation** | Review `ml/eval.py`: loads model, runs on test speaker, computes metrics |
| 1512 | **Trace — Metric computation** | Verify: accuracy, F1-macro, per-class precision/recall, confusion matrix |
| 1513 | **Specify — Eval protocol** | Float model eval on test speaker; int8 model eval on same; report both |
| 1514 | **Implement — Per-fold evaluation** | `ml/eval.py` runs on each fold's test speaker; outputs JSON metrics |
| 1515 | **Test — Evaluation consistency** | Run eval twice on same fold → identical metrics (deterministic) |
| 1516 | **Run — 3-fold evaluation** | Execute for all 3 folds; collect per-fold + aggregate metrics |
| 1517 | **Review — Evaluation report** | `docs/EVALUATION_REPORT.md`: per-fold + mean±std tables, confusion matrices |
| 1518 | **Document — Float model metrics** | `results/float_eval_fold_{1,2,3}.json` + `results/float_eval_aggregate.json` |
| 1519 | **Integrate — Eval in training loop** | `ml/train.py` calls eval on best checkpoint |
| 1520 | **Gate — Float evaluation complete** | All 3 folds evaluated; metrics archived; aggregate computed |

### Phase 16.3: Int8 Quantization & Export (1521–1560)

| Step | Title | Acceptance |
|------|-------|------------|
| 1521 | **Inspect — Quantization pipeline** | Review `ml/export_tflite.py`: representative dataset, full int8, INT8 ops only |
| 1522 | **Trace — Calibration data** | Representative dataset: 100 samples from training set (balanced across classes) |
| 1523 | **Specify — Quantization targets** | Full int8 (weights + activations); input/output int8; size < 50KB; accuracy drop < 1% |
| 1524 | **Implement — Quantization per fold** | Export 3 int8 models (one per fold's best checkpoint) |
| 1525 | **Test — Quantization accuracy** | Evaluate each int8 model on its test speaker; compare to float baseline |
| 1526 | **Run — Quantization sweep** | If accuracy drop > 1%: quantization-aware training (QAT) → re-export |
| 1527 | **Review — Quantization report** | `docs/QUANTIZATION_REPORT.md`: per-fold float vs int8 accuracy, model sizes |
| 1528 | **Document — Int8 models** | `ml/model_int8_fold_{1,2,3}.tflite` + `ml/quantization_config.json` |
| 1529 | **Integrate — Best int8 model selection** | Select fold with highest int8 accuracy for firmware integration |
| 1530 | **Gate — Int8 export complete** | 3 int8 models exported; accuracy drop < 1%; size < 50KB |

### Phase 16.4: Firmware Integration & On-Device Validation (1531–1580)

| Step | Title | Acceptance |
|------|-------|------------|
| 1531 | **Inspect — TFLite-Micro integration** | Review `firmware/main/infer_task.c`: model embedding, arena size, op resolver |
| 1532 | **Trace — Memory budget** | Model (20KB) + arena (8KB) + tensors + stack < 200KB SRAM |
| 1533 | **Specify — Integration procedure** | Convert `.tflite` → C array (`xxd -i`); update `model_data.h`; rebuild firmware |
| 1534 | **Implement — Model embedding** | `scripts/embed_model.py`: converts `.tflite` → `model_int8_tflite.h` |
| 1534 | **Test — Firmware rebuild** | `idf.py build` succeeds; binary size increase matches model |
| 1535 | **Run — Flash & inference test** | Flash firmware; send test MFCC via USB → verify inference output matches PC |
| 1536 | **Run — On-device accuracy test** | 50 test MFCC vectors → compare device predictions to PC float/int8 |
| 1537 | **Review — On-device validation** | `docs/ON_DEVICE_VALIDATION.md`: latency, memory, accuracy vs. PC |
| 1538 | **Document — Firmware model integration** | `docs/FIRMWARE_MODEL_INTEGRATION.md` |
| 1539 | **Integrate — Model in firmware** | `model_int8_tflite.h` committed; firmware builds with model |
| 1540 | **Gate — Model runs on device** | Inference latency < 50ms; accuracy matches PC int8; SRAM within budget |

### Phase 16.5: Model Card & Release (1541–1600)

| Step | Title | Acceptance |
|------|-------|------------|
| 1541 | **Inspect — Model card template** | Review `ml/model_card.md` sections |
| 1542 | **Trace — Card population** | Auto-fill from training/eval/quantization logs |
| 1543 | **Specify — Card completeness** | All sections: model details, intended use, training data, metrics, ethics, limitations |
| 1544 | **Implement — Card generator** | `scripts/generate_model_card.py`: reads results → writes `ml/model_card.md` |
| 1545 | **Test — Card completeness** | All sections filled; no TBD placeholders |
| 1546 | **Run — Card generation** | Produces final `ml/model_card.md` with actual metrics |
| 1547 | **Review — Card review** | Peer review: accuracy honesty, limitations explicit, consent documented |
| 1548 | **Document — Final model card** | `ml/model_card.md` v1.0.0 |
| 1549 | **Integrate — Model card in repo** | Committed; linked in README |
| 1550 | **Gate — Model card complete** | Professional model card published with all evidence |

---

## Phase 17 — Physical ESP32/Linux Integration (Steps 1601–1700)

**Objective:** Demonstrate the complete voice-to-action chain on physical hardware.

### Phase 17.1: End-to-End Pipeline Integration (1601–1650)

| Step | Title | Acceptance |
|------|-------|------------|
| 1601 | **Inspect — Full pipeline components** | Verify: mic → I2S → GDMA → MFCC → VAD → TFLite-Micro → intent → USB CDC → host |
| 1602 | **Trace — Data flow timing** | Instrument: each stage timestamp → end-to-end latency breakdown |
| 1603 | **Specify — Integration targets** | PTT → result < 800ms p99; zero frame drops; host receives valid frames |
| 1604 | **Implement — Firmware integration** | Enable infer_task with real model; connect all FreeRTOS queues |
| 1605 | **Test — Pipeline bring-up** | Press PTT → speak → verify: intent classified → frame sent → host ACK |
| 1606 | **Run — Pipeline latency measurement** | 100 PTT cycles; oscilloscope + host timestamps; latency p50/p95/p99 |
| 1607 | **Review — Pipeline integration report** | `docs/PIPELINE_INTEGRATION_HW_REPORT.md`: latency, success rate, errors |
| 1608 | **Document — HW pipeline evidence** | `results/pipeline_integration_hw.json` with `MEASURED` label |
| 1609 | **Integrate — Full pipeline on hardware** | `make hw-pipeline-test` target |
| 1610 | **Gate — E2E pipeline on hardware** | Success rate > 95%; latency < 800ms p99; `MEASURED` evidence |

### Phase 17.2: Host Integration & Demo (1611–1660)

| Step | Title | Acceptance |
|------|-------|------------|
| 1611 | **Inspect — Host readiness** | Verify: `make sim-demo` works; host_agent.py handles physical CDC device |
| 1602 | **Trace — Host-device handshake** | Physical: device boots → TIME_SYNC → host ACK → PING → host ACK → ready |
| 1613 | **Specify — Demo script** | Define: exact phrases, expected actions, success criteria |
| 1614 | **Implement — Physical demo script** | `tools/physical_demo.py`: automates demo sequence, captures evidence |
| 1615 | **Test — Single command demo** | "Open amplifier and run simulation" → host opens project → runs ngspice → result |
| 1616 | **Run — Full demo sequence** | 5 commands: open/run, show result, run again, yesterday, cancel |
| 1617 | **Review — Physical demo report** | `docs/PHYSICAL_DEMO_REPORT.md`: transcript, latency, success/fail per command |
| 1618 | **Document — Physical demo evidence** | `results/physical_demo.json` with `MEASURED` label; photos, screen recording |
| 1619 | **Integrate — Demo in Makefile** | `make hw-demo` target |
| 1620 | **Gate — Physical demo works** | All 5 commands succeed; latency measured; evidence archived |

### Phase 17.3: Stress & Reliability Testing (1621–1700)

| Step | Title | Acceptance |
|------|-------|------------|
| 1621 | **Inspect — Reliability test matrix** | Define: 1000 PTT cycles, cable wiggle, host restart, device reboot, power cycle |
| 1622 | **Trace — Failure modes** | Map: CRC error → NACK → retry; cable unplug → reconnect handshake; host crash → recovery |
| 1623 | **Specify — Reliability targets** | MTBF > 1000 commands; recovery < 5s; zero data corruption |
| 1624 | **Implement — Stress test harness** | `tools/stress_test.py`: automated sequence, logs every command/response |
| 1624 | **Test — 1000-cycle stress** | Run overnight; log success/fail, latency, errors, recovery times |
| 1625 | **Run — Fault injection** | Cable unplug mid-transaction; host kill -9; power cycle device |
| 1625 | **Run — Thermal soak** | 1 hour continuous operation; monitor temperature, current, stability |
| 1626 | **Review — Stress test report** | `docs/STRESS_TEST_REPORT.md`: MTBF, recovery times, error analysis |
| 1627 | **Document — Reliability evidence** | `results/stress_test.json` with `MEASURED` label |
| 1628 | **Integrate — Reliability in CI** | `make hw-stress-test` target |
| 1629 | **Gate — Reliability validated** | MTBF target met; all fault scenarios recover; evidence archived |

---

## Phase 18 — Local LLM & Agent Runtime (Steps 1701–1800)

**Objective:** Deploy a small local LLM on the Linux host for task planning and contextual reasoning.

### Phase 18.1: LLM Selection & Deployment (1701–1740)

| Step | Title | Acceptance |
|------|-------|------------|
| 1701 | **Inspect — LLM candidates** | Evaluate: llama.cpp (7B/13B GGUF), Ollama, vLLM; criteria: CPU-only, < 8GB RAM, < 5s latency |
| 1702 | **Trace — Integration architecture** | LLM proposes actions → verification layer → execution layer → result → context update |
| 1703 | **Specify — LLM interface** | REST/gRPC/stdio; structured output (JSON schema); timeout, retry, streaming |
| 1704 | **Implement — LLM server** | `host/llm/server.py`: loads model, exposes `/generate` endpoint, health check |
| 1705 | **Test — LLM basic inference** | Prompt: "Plan: open amplifier project and run simulation" → structured action plan |
| 1706 | **Run — Latency benchmark** | 50 prompts; measure p50/p95 latency, tokens/sec, memory usage |
| 1707 | **Review — LLM deployment report** | `docs/LLM_DEPLOYMENT_REPORT.md`: model, quantization, latency, hardware reqs |
| 1708 | **Document — LLM integration guide** | `docs/LLM_INTEGRATION.md`: install, config, API, troubleshooting |
| 1709 | **Integrate — LLM in host stack** | `host/llm/` package; `host_agent.py` imports LLM client |
| 1710 | **Gate — LLM operational** | Model loads, responds to prompts, latency < 5s, runs on target hardware |

### Phase 18.2: Task Planner & Verification Layer (1711–1760)

| Step | Title | Acceptance |
|------|-------|------------|
| 1711 | **Inspect — Planner requirements** | Input: user intent + context; Output: ordered action list with params, preconditions |
| 1712 | **Trace — Verification layer** | Every LLM action → schema validation → allow-list check → confirmation gate → execution |
| 1713 | **Specify — Action schema** | JSON schema: action_type, params, preconditions, effects, rollback, confirmation_required |
| 1714 | **Implement — Planner module** | `host/planner.py`: LLM prompt → structured output → validation → action objects |
| 1715 | **Implement — Verification layer** | `host/verifier.py`: schema → allow-list → path jail → risk check → confirmation queue |
| 1716 | **Test — Planner accuracy** | 50 intents → compare planned actions to ground truth; target > 95% correct |
| 1717 | **Run — End-to-end planning** | Voice intent → LLM plan → verification → host dispatch → result |
| 1718 | **Review — Planner report** | `docs/PLANNER_REPORT.md`: accuracy, latency, failure modes |
| 1719 | **Document — Planner API** | `docs/PLANNER_API.md` |
| 1720 | **Integrate — Planner in host_agent** | `host_agent.py` routes intent through planner+verifier |
| 1721 | **Gate — Planner operational** | 50 test intents → >95% correct plans; all verified before execution |

### Phase 18.3: Contextual Retrieval & Memory (1721–1780)

| Step | Title | Acceptance |
|------|-------|------------|
| 1721 | **Inspect — Context store evolution** | Current: 16-event ring buffer; Need: vector search, semantic retrieval, cross-session |
| 1722 | **Trace — Vector DB options** | Evaluate: Chroma, FAISS, SQLite-vec; criteria: local, no server, Python, < 100MB |
| 1723 | **Specify — Memory architecture** | Short-term: ring buffer (existing); Long-term: vector DB + metadata; Retrieval: hybrid |
| 1724 | **Implement — Vector store** | `host/memory/vector_store.py`: Chroma/FAISS wrapper; embeddings via sentence-transformers |
| 1725 | **Implement — Contextual retrieval** | `host/memory/retriever.py`: query → vector search → re-rank → top-k context snippets |
| 1726 | **Test — Retrieval quality** | 50 queries → manual relevance judgment; target > 80% relevant in top-3 |
| 1727 | **Run — Cross-session persistence** | Restart host → query "what did I simulate yesterday?" → correct context retrieved |
| 1728 | **Review — Memory report** | `docs/MEMORY_REPORT.md`: architecture, retrieval metrics, persistence test |
| 1729 | **Document — Memory API** | `docs/MEMORY_API.md` |
| 1730 | **Integrate — Memory in planner** | Planner injects retrieved context into LLM prompt |
| 1731 | **Gate — Memory operational** | Retrieval latency < 200ms; cross-session persistence verified |

### Phase 18.4: LLM Safety & Guardrails (1731–1800)

| Step | Title | Acceptance |
|------|-------|------------|
| 1731 | **Inspect — Safety risks** | Prompt injection, hallucinated actions, path escape, resource exhaustion |
| 1732 | **Trace — Guardrail layers** | Input sanitization → schema validation → allow-list → confirmation → execution sandbox |
| 1733 | **Specify — Guardrail implementation** | Input: length limit, character filter; Output: schema validation → verifier → executor |
| 1734 | **Implement — Guardrails** | `host/guardrails.py`: input sanitizer, output validator, rate limiter, token budget |
| 1734 | **Test — Adversarial prompts** | 100 adversarial inputs (injection, escape, DoS) → all blocked or safe |
| 1735 | **Run — Safety benchmark** | `tools/safety_benchmark.py`: automated adversarial suite |
| 1736 | **Review — Safety report** | `docs/SAFETY_REPORT.md`: attack vectors, mitigations, residual risk |
| 1737 | **Document — Guardrail config** | `host/guardrails_config.yaml` |
| 1738 | **Integrate — Guardrails in pipeline** | All LLM I/O passes through guardrails |
| 1739 | **Gate — Safety validated** | 100 adversarial tests pass; no unsafe actions executed |

---

## Phase 19 — Desktop Automation & Tool Orchestration (Steps 1801–1900)

**Objective:** Controlled execution of actual electronics workflows (KiCad, ngspice, file ops) via the agent.

### Phase 19.1: Tool Registry & Adapters (1801–1840)

| Step | Title | Acceptance |
|------|-------|------------|
| 1801 | **Inspect — Tool landscape** | Inventory: KiCad CLI, ngspice, git, file ops, shell (restricted), Python scripts |
| 1802 | **Trace — Adapter pattern** | Each tool → Python adapter class: `validate()`, `execute()`, `parse_output()`, `rollback()` |
| 1803 | **Specify — Tool adapter interface** | Base class `ToolAdapter`; required methods; timeout, retry, error handling |
| 1804 | **Implement — Ngspice adapter** | `host/tools/ngspice_adapter.py`: runs simulation, parses `.meas`, returns structured results |
| 1804 | **Implement — KiCad adapter** | `host/tools/kicad_adapter.py`: open project, run ERC/DRC, export BOM/gerbers |
| 1805 | **Implement — File ops adapter** | `host/tools/file_adapter.py`: read/write/list/delete with path jail |
| 1805 | **Implement — Git adapter** | `host/tools/git_adapter.py`: status, diff, commit, tag (read-only by default) |
| 1806 | **Test — Adapter unit tests** | Each adapter: valid input → success; invalid → structured error; timeout → killed |
| 1807 | **Run — Adapter integration test** | Chain: KiCad open → ngspice run → file read → result parsed |
| 1808 | **Review — Adapter report** | `docs/TOOL_ADAPTERS_REPORT.md`: coverage, latency, error handling |
| 1809 | **Document — Tool registry** | `docs/TOOL_REGISTRY.md`: available tools, schemas, examples |
| 1810 | **Integrate — Registry in planner** | Planner selects tools by name; registry instantiates adapters |
| 1811 | **Gate — Tool registry operational** | All adapters tested; planner can invoke any tool |

### Phase 19.2: Confirmation Gates & Approval Workflows (1811–1850)

| Step | Title | Acceptance |
|------|-------|------------|
| 1811 | **Inspect — Confirmation requirements** | Destructive: file delete, git push, KiCad PCB edit, shell command → require approval |
| 1812 | **Trace — Approval flow** | Planner → confirmation queue → UI prompt (CLI/desktop) → user yes/no → execute/abort |
| 1813 | **Specify — Approval UI** | CLI: `input()` prompt; Desktop: tkinter/zenity dialog; Headless: auto-approve safe actions |
| 1814 | **Implement — Confirmation queue** | `host/approval/queue.py`: thread-safe; timeout; audit log |
| 1815 | **Implement — CLI approval UI** | `host/approval/cli.py`: colored prompt, default no, audit log |
| 1815 | **Implement — Desktop approval UI** | `host/approval/desktop.py`: zenity/kdialog; fallback to CLI |
| 1816 | **Test — Approval flow** | Planner requests delete → prompt appears → yes → execute; no → abort logged |
| 1816 | **Run — Approval integration test** | Full chain: plan → confirm → execute → result logged |
| 1817 | **Review — Approval report** | `docs/APPROVAL_WORKFLOW_REPORT.md`: flow, timeout, audit |
| 1817 | **Document — Approval config** | `host/approval/config.yaml`: timeouts, defaults, auto-approve safe actions |
| 1818 | **Integrate — Approval in executor** | Executor pauses on risky action → waits for approval → continues |
| 1818 | **Gate — Approval gates operational** | All risky actions require approval; audit trail complete |

### Phase 19.3: Execution Engine & Result Verification (1819–1880)

| Step | Title | Acceptance |
|------|-------|------------|
| 1819 | **Inspect — Execution requirements** | Sequential/parallel actions; dependency resolution; rollback on failure |
| 1820 | **Trace — Execution lifecycle** | Plan → resolve deps → confirm → execute → verify → commit/rollback → audit |
| 1821 | **Specify — Executor interface** | `execute(plan) -> result`; handles: parallel groups, retries, timeouts, partial failure |
| 1822 | **Implement — Executor core** | `host/executor.py`: DAG execution; topological sort; per-action timeout; rollback hooks |
| 1822 | **Implement — Result verification** | Each action: `verify()` method; compares actual output to expected schema |
| 1823 | **Implement — Rollback manager** | `host/executor/rollback.py`: compensating actions (delete created files, git reset) |
| 1823 | **Test — Executor scenarios** | Success chain; single failure → rollback; timeout → partial rollback; dependency order |
| 1824 | **Run — Executor stress test** | 50 random plans; verify: atomicity, audit completeness, no orphan resources |
| 1824 | **Run — Verification accuracy** | 100 actions → compare `verify()` to manual check; target 100% |
| 1825 | **Review — Executor report** | `docs/EXECUTOR_REPORT.md`: atomicity, rollback success, latency |
| 1826 | **Document — Executor API** | `docs/EXECUTOR_API.md` |
| 1826 | **Integrate — Executor in host_agent** | Planner → verifier → executor → result → context update |
| 1827 | **Gate — Execution engine operational** | All test scenarios pass; atomicity guaranteed; audit complete |

### Phase 19.4: Desktop GUI Integration (1828–1900)

| Step | Title | Acceptance |
|------|-------|------------|
| 1828 | **Inspect — GUI framework options** | Tkinter (stdlib), PyQt, Electron; criteria: cross-platform, lightweight, Python |
| 1829 | **Trace — GUI requirements** | Status dashboard, approval dialogs, project browser, log viewer, voice activity |
| 1830 | **Specify — GUI architecture** | Main window + dialogs; MVC; async updates from host_agent via queue |
| 1831 | **Implement — Main window** | `host/gui/main.py`: status panel, project list, log tail, PTT indicator |
| 1831 | **Implement — Approval dialog** | Reuses `host/approval/desktop.py`; modal, blocking, audible alert |
| 1832 | **Implement — Project browser** | Tree view: projects → files; double-click → open in KiCad/editor |
| 1832 | **Implement — Log viewer** | Real-time tail of audit log; filter by direction/verb/error |
| 1833 | **Test — GUI functionality** | Launch → all panels render; approval dialog blocks correctly; log updates live |
| 1834 | **Run — GUI integration test** | Full demo: voice → plan → GUI approval → execute → result in log |
| 1835 | **Review — GUI report** | `docs/GUI_REPORT.md`: responsiveness, usability, resource usage |
| 1836 | **Document — GUI user guide** | `docs/GUI_USER_GUIDE.md` |
| 1837 | **Integrate — GUI launch** | `make gui` target; auto-starts with host_agent |
| 1838 | **Gate — Desktop GUI operational** | All panels functional; approval flow works; no crashes in 1h test |

---

## Phase 20 — Persistent Contextual Memory & Task Recovery (Steps 1901–2000)

**Objective:** Cross-session project memory, task continuity, and intelligent LAST/YESTERDAY resolution.

### Phase 20.1: Long-Term Vector Memory (1901–1940)

| Step | Title | Acceptance |
|------|-------|------------|
| 1901 | **Inspect — Current context limits** | 16-event ring buffer; no semantic search; no cross-session |
| 1902 | **Trace — Memory requirements** | Semantic search over project history; LAST/YESTERDAY via embeddings; multi-project |
| 1903 | **Specify — Memory schema** | Event: id, timestamp, project, action, result, embedding, tags, session_id |
| 1904 | **Implement — Vector store backend** | `host/memory/vector_store.py`: Chroma persistence; collection per project |
| 1904 | **Implement — Embedding pipeline** | `host/memory/embedder.py`: sentence-transformers (all-MiniLM-L6-v2); batch encode |
| 1905 | **Implement — Memory writer** | On PROJECT_EVENT → create event → embed → store in vector DB |
| 1905 | **Test — Memory write/read** | 100 events → query by text → relevant events in top-5 |
| 1906 | **Run — Cross-session persistence** | Restart host → query "last simulation" → correct project retrieved |
| 1907 | **Review — Memory report** | `docs/VECTOR_MEMORY_REPORT.md`: latency, recall, storage size |
| 1907 | **Document — Vector memory API** | `docs/VECTOR_MEMORY_API.md` |
| 1908 | **Integrate — Vector memory in host** | `HostSession` uses vector store for LAST/YESTERDAY resolution |
| 1909 | **Gate — Vector memory operational** | Cross-session retrieval works; latency < 200ms; storage < 100MB |

### Phase 20.2: Intelligent LAST/YESTERDAY Resolution (1910–1950)

| Step | Title | Acceptance |
|------|-------|------------|
| 1910 | **Inspect — Current resolution** | Exact match on `local_day` (YESTERDAY) or most recent (LAST) |
| 1911 | **Trace — Ambiguity cases** | Multiple simulations same day → YESTERDAY ambiguous; no history → LAST fails |
| 1912 | **Specify — Semantic resolution** | LAST: most recent simulation (any project); YESTERDAY: most recent on previous day |
| 1913 | **Implement — Semantic resolver** | `host/memory/resolver.py`: vector search + temporal filter + recency ranking |
| 1914 | **Implement — Fallback chain** | Semantic → temporal exact → most recent → confirm required |
| 1915 | **Test — Resolution accuracy** | 50 queries: "last", "yesterday", "day before" → manual judgment > 90% correct |
| 1916 | **Run — Edge case testing** | Empty history, multiple same-day, cross-project, timezone change |
| 1917 | **Review — Resolver report** | `docs/SEMANTIC_RESOLVER_REPORT.md`: accuracy, latency, edge cases |
| 1918 | **Document — Resolver API** | `docs/SEMANTIC_RESOLVER_API.md` |
| 1919 | **Integrate — Resolver in host_agent** | `_project("LAST")` and `_project("YESTERDAY")` use semantic resolver |
| 1920 | **Gate — Semantic resolution operational** | 50 queries > 90% correct; fallback chain works; latency < 100ms |

### Phase 20.3: Task State Recovery & Continuity (1921–1980)

| Step | Title | Acceptance |
|------|-------|------------|
| 1921 | **Inspect — Task state model** | Current: none; Need: in-progress task, completed steps, pending actions, checkpoints |
| 1922 | **Trace — Recovery scenarios** | Host crash mid-plan → restart → resume from last checkpoint; device reboot → context sync |
| 1923 | **Specify — Task state schema** | Task: id, plan, current_step, completed_steps, checkpoints, created, updated |
| 1924 | **Implement — Task state store** | `host/memory/task_store.py`: SQLite persistence; checkpoint on each step completion |
| 1924 | **Implement — Recovery logic** | On startup: load incomplete tasks → prompt "Resume task X?" → continue from checkpoint |
| 1925 | **Test — Crash recovery** | Kill host mid-plan → restart → resume from last checkpoint → completes correctly |
| 1925 | **Test — Device reboot sync** | Device reboots → host receives TIME_SYNC → PROJECT_EVENT sync → context consistent |
| 1926 | **Run — End-to-end recovery** | Full scenario: plan → execute 3/5 steps → crash → restart → resume → complete |
| 1927 | **Review — Recovery report** | `docs/TASK_RECOVERY_REPORT.md`: scenarios, success rate, time to resume |
| 1927 | **Document — Task recovery API** | `docs/TASK_RECOVERY_API.md` |
| 1928 | **Integrate — Recovery in host_agent** | Startup checks task store; offers resume; executor checkpoints |
| 1929 | **Gate — Task recovery operational** | Crash/resume works; device sync works; no data loss |

### Phase 20.4: Context-Aware Intelligence (1931–2000)

| Step | Title | Acceptance |
|------|-------|------------|
| 1931 | **Inspect — Context injection** | Current: none; Need: planner receives relevant history for better plans |
| 1932 | **Trace — Context relevance** | Query: "simulate the amplifier again" → retrieve last amplifier simulation params |
| 1933 | **Specify — Context retrieval for planning** | Planner query → vector search (project + action + time) → top-k context → LLM prompt |
| 1934 | **Implement — Context retriever for planner** | `host/memory/planner_retriever.py`: query rewrite → vector search → re-rank → format |
| 1934 | **Test — Context relevance** | 30 planning queries → retrieved context manually judged relevant > 85% |
| 1935 | **Run — Planning with context** | "simulate it again" → retrieves last sim → planner uses params → correct action |
| 1935 | **Run — Multi-project context** | Switch projects → context isolates per project → no leakage |
| 1936 | **Review — Context intelligence report** | `docs/CONTEXT_INTELLIGENCE_REPORT.md`: relevance, latency, multi-project isolation |
| 1936 | **Document — Context-aware planning API** | `docs/CONTEXT_PLANNING_API.md` |
| 1937 | **Integrate — Context in planner** | Planner always queries retriever before LLM call |
| 1938 | **Gate — Context-aware planning operational** | 30 queries > 85% relevant context; planner uses context correctly |

---

## Phase 21 — Live Monitoring Dashboard (Steps 2001–2100)

**Objective:** Real-time observability of device, agent, and execution state.

### Phase 21.1: Telemetry Infrastructure (2001–2040)

| Step | Title | Acceptance |
|------|-------|------------|
| 2001 | **Inspect — Telemetry sources** | Device: MCU stats, audio levels, inference latency, queue depths; Host: CPU, RAM, LLM latency, plan status |
| 2002 | **Trace — Telemetry transport** | Device → host: USB CDC telemetry frames; Host → dashboard: WebSocket/HTTP |
| 2003 | **Specify — Telemetry protocol** | JSON frames: `{"source": "device|host", "metric": "...", "value": ..., "ts": ...}` |
| 2004 | **Implement — Device telemetry** | Firmware: periodic task → encode telemetry → USB CDC (low priority queue) |
| 2004 | **Implement — Host telemetry collector** | `host/telemetry/collector.py`: receives device frames + host metrics → buffers |
| 2005 | **Test — Telemetry pipeline** | Device sends → host receives → buffers → dashboard updates in real-time |
| 2006 | **Run — Telemetry latency** | End-to-end: device metric → dashboard < 200ms |
| 2007 | **Review — Telemetry report** | `docs/TELEMETRY_REPORT.md`: bandwidth, latency, reliability |
| 2008 | **Document — Telemetry protocol** | `docs/TELEMETRY_PROTOCOL.md` |
| 2009 | **Integrate — Telemetry in stack** | Device task + host collector auto-start |
| 2010 | **Gate — Telemetry operational** | Device + host metrics flow to dashboard in real-time |

### Phase 21.2: Dashboard Frontend (2011–2060)

| Step | Title | Acceptance |
|------|-------|------------|
| 2011 | **Inspect — Dashboard tech stack** | Options: React + Vite, Streamlit, Dash, Tauri; criteria: real-time, Python backend, low resource |
| 2012 | **Trace — Dashboard requirements** | Panels: device status, audio levels, inference latency, host CPU/RAM, plan progress, audit log |
| 2013 | **Specify — Dashboard architecture** | Backend: FastAPI + WebSocket; Frontend: React + Recharts; Deploy: single binary |
| 2014 | **Implement — Backend API** | `host/dashboard/api.py`: FastAPI + WebSocket; serves telemetry, history, controls |
| 2014 | **Implement — Frontend** | `host/dashboard/frontend/`: React + Vite + Recharts; real-time charts, status badges |
| 2015 | **Test — Dashboard functionality** | Launch → all panels render; WebSocket connects; data updates live |
| 2016 | **Run — Dashboard integration** | Start host_agent + dashboard → all panels show live data |
| 2017 | **Review — Dashboard UX** | `docs/DASHBOARD_UX_REPORT.md`: usability, responsiveness, resource usage |
| 2018 | **Document — Dashboard deployment** | `docs/DASHBOARD_DEPLOYMENT.md`: build, run, configure |
| 2019 | **Integrate — Dashboard launch** | `make dashboard` target; auto-starts with host_agent |
| 2020 | **Gate — Dashboard operational** | All panels functional; real-time updates; < 5% CPU overhead |

### Phase 21.3: Alerting & Diagnostics (2021–2080)

| Step | Title | Acceptance |
|------|-------|------------|
| 2021 | **Inspect — Alerting needs** | Device disconnect, inference failure, host CPU spike, queue overflow, audit errors |
| 2022 | **Trace — Alert channels** | Dashboard toast, desktop notification, log entry, audible beep |
| 2023 | **Specify — Alert rules** | Thresholds: device silent > 30s, inference > 100ms, host CPU > 90%, queue > 80% |
| 2024 | **Implement — Alert engine** | `host/dashboard/alerts.py`: rule eval, dedup, escalation, notification dispatch |
| 2024 | **Implement — Notification channels** | Dashboard toast (WebSocket), desktop notify (libnotify), log (audit) |
| 2025 | **Test — Alert firing** | Inject each condition → alert fires within 5s; dedup works |
| 2026 | **Run — Alert soak test** | 1 hour normal operation → zero false positives; inject faults → all caught |
| 2027 | **Review — Alerting report** | `docs/ALERTING_REPORT.md`: rules, false positive rate, notification latency |
| 2028 | **Document — Alert config** | `host/dashboard/alerts_config.yaml` |
| 2029 | **Integrate — Alerts in dashboard** | Alerts panel shows active/fired; history searchable |
| 2030 | **Gate — Alerting operational** | All critical conditions alert; zero missed in soak test |

### Phase 21.4: Historical Analysis & Reporting (2031–2100)

| Step | Title | Acceptance |
|------|-------|------------|
| 2031 | **Inspect — Historical data** | Telemetry buffered in memory; Need: persistence, query, export |
| 2032 | **Trace — Storage backend** | Options: SQLite, InfluxDB, TimescaleDB; criteria: local, embedded, SQL, retention |
| 2033 | **Specify — History schema** | Tables: metrics (ts, source, metric, value), events (ts, type, details) |
| 2034 | **Implement — History store** | `host/dashboard/history.py`: SQLite + pandas; automatic partitioning by day |
| 2034 | **Implement — Query API** | `host/dashboard/history_api.py`: time range, metric filter, aggregation |
| 2035 | **Test — History queries** | Dashboard: "last hour latency p99" → chart renders in < 2s |
| 2036 | **Run — Report generation** | `host/dashboard/reports.py`: daily/weekly PDF: latency trends, error counts, uptime |
| 2037 | **Review — Historical analysis** | `docs/HISTORICAL_ANALYSIS_REPORT.md`: trends, anomalies, capacity planning |
| 2037 | **Document — History API** | `docs/HISTORY_API.md` |
| 2038 | **Integrate — History in dashboard** | Charts: "Last 24h", "Last 7d"; export CSV/PDF buttons |
| 2039 | **Gate — Historical analysis operational** | Queries < 2s; reports generate; retention 30 days |

---

## Phase 22 — Reliability, Security & Fault Injection (Steps 2101–2200)

**Objective:** Harden the integrated system against communication faults, adversarial inputs, and hardware failures.

### Phase 22.1: Communication Fault Hardening (2101–2140)

| Step | Title | Acceptance |
|------|-------|------------|
| 2101 | **Inspect — Current fault coverage** | CRC, malformed, oversize, fuzz tested in sim; Need: physical layer faults |
| 2102 | **Trace — Physical fault modes** | Cable unplug, connector wiggle, EMI, voltage droop, USB suspend/resume |
| 2103 | **Specify — Fault injection harness** | Hardware: USB port power control, cable breakout board; Software: fault scheduler |
| 2104 | **Implement — Physical fault injector** | `tools/fault_injector.py`: controls USB hub power, schedules faults during test |
| 2104 | **Implement — Fault scenarios** | Cable pull mid-frame; voltage droop 10%; EMI burst; suspend/resume cycle |
| 2105 | **Test — Fault injection** | Run each scenario 50×; verify: recovery, no data corruption, latency bounded |
| 2106 | **Run — Automated fault suite** | `make hw-fault-test`: sequences all scenarios, logs outcomes |
| 2107 | **Review — Fault hardening report** | `docs/COMM_FAULT_HARDENING_REPORT.md`: MTBF, recovery time, residual failures |
| 2107 | **Document — Fault injector guide** | `docs/FAULT_INJECTOR_GUIDE.md` |
| 2108 | **Integrate — Fault tests in CI** | `make hw-fault-test` target |
| 2108 | **Gate — Comm fault hardened** | All scenarios recover; MTBF > 1000 commands; zero data loss |

### Phase 22.2: Security Hardening (2109–2150)

| Step | Title | Acceptance |
|------|-------|------------|
| 2109 | **Inspect — Security surface** | USB descriptors, firmware update, NVS, LLM prompt injection, tool execution |
| 2110 | **Trace — Threat model update** | STRIDE: Spoofing (device), Tampering (firmware), Repudiation (audit), Info disclosure (NVS), DoS (queue), Elevation (shell) |
| 2111 | **Specify — Mitigations** | Signed firmware, NVS encryption, rate limiting, sandboxed execution, audit integrity |
| 2112 | **Implement — Signed firmware** | `scripts/sign_firmware.py`: ED25519; bootloader verifies; `idf.py` integration |
| 2112 | **Implement — NVS encryption** | ESP32-S3 flash encryption + NVS encrypted partition; key in eFuse |
| 2113 | **Implement — Rate limiting** | Host: per-action limits; Device: frame rate limit; LLM: token budget |
| 2113 | **Implement — Sandbox execution** | Tool adapters: subprocess with `seccomp` profile; no network, restricted FS |
| 2114 | **Test — Security verification** | `tools/security_test.py`: unsigned firmware rejected; NVS unreadable; sandbox escapes blocked |
| 2115 | **Run — Penetration test** | External reviewer: 2 hours black-box; report findings |
| 2115 | **Review — Security hardening report** | `docs/SECURITY_HARDENING_REPORT.md`: mitigations, residual risk, compliance |
| 2116 | **Document — Security config** | `docs/SECURITY_CONFIG.md`: keys, certificates, policies |
| 2116 | **Integrate — Hardened build** | `make secure-build` target; produces signed, encrypted firmware |
| 2117 | **Gate — Security hardened** | All mitigations implemented; pen test clean; secure build produces bootable image |

### Phase 22.3: System Recovery & Watchdogs (2118–2180)

| Step | Title | Acceptance |
|------|-------|------------|
| 2118 | **Inspect — Recovery mechanisms** | Current: NVS backup, host task checkpoints; Need: device watchdog, host health monitor |
| 2119 | **Trace — Failure scenarios** | Device freeze, host OOM, LLM timeout, queue deadlock, NVS corruption |
| 2120 | **Specify — Recovery architecture** | Device: HW watchdog + SW task monitor; Host: systemd watchdog + health endpoint |
| 2121 | **Implement — Device watchdog** | ESP32-S3 HW WDT: 30s timeout; task check-in every 10s; reset on timeout |
| 2121 | **Implement — Host health monitor** | `host/health_monitor.py`: systemd watchdog; `/health` endpoint; auto-restart on failure |
| 2122 | **Implement — NVS corruption recovery** | On boot: `nvs_flash_init` → if corrupt → erase + reinit; context rebuild from host |
| 2122 | **Test — Recovery scenarios** | Device freeze → WDT reset → host reconnect → context sync; Host OOM → systemd restart |
| 2123 | **Run — Recovery soak test** | 24 hours with injected faults; all recover automatically; zero manual intervention |
| 2123 | **Review — Recovery report** | `docs/SYSTEM_RECOVERY_REPORT.md`: scenarios, recovery times, success rate |
| 2124 | **Document — Recovery procedures** | `docs/RECOVERY_PROCEDURES.md` |
| 2124 | **Integrate — Recovery in production build** | Watchdogs enabled by default; health monitor auto-starts |
| 2125 | **Gate — System self-healing** | All fault scenarios recover automatically; zero data loss; < 30s recovery |

### Phase 22.4: Compliance & Audit Trail (2126–2200)

| Step | Title | Acceptance |
|------|-------|------------|
| 2126 | **Inspect — Audit requirements** | Immutable log, tamper evidence, retention, export, verification |
| 2127 | **Trace — Audit chain** | Current: JSONL append-only; Need: cryptographic chaining, Merkle tree, verification |
| 2128 | **Specify — Audit integrity** | Hash chain: each entry includes prev_hash; periodic anchor to external timestamp |
| 2129 | **Implement — Tamper-evident log** | `host/audit_log_v2.py`: SHA-256 chain; daily anchor to git commit hash |
| 2129 | **Implement — Log verification** | `tools/verify_audit_log.py`: validates chain; detects truncation/tampering |
| 2130 | **Test — Audit integrity** | Truncate log → verify detects; modify entry → verify detects; append → chain valid |
| 2131 | **Run — Audit soak** | 1 month continuous → verify chain intact; export/import round-trip |
| 2131 | **Review — Audit compliance report** | `docs/AUDIT_COMPLIANCE_REPORT.md`: chain validity, retention, export format |
| 2131 | **Document — Audit spec v2** | `docs/AUDIT_SPEC_v2.md`: format, verification, retention policy |
| 2132 | **Integrate — Tamper-evident audit** | `host_agent.py` uses v2 logger; `make audit` runs verification |
| 2133 | **Gate — Audit trail tamper-proof** | Chain verification passes; tampering detected; export/import works |

---

## Phase 23 — Actual Performance Benchmarking (Steps 2201–2300)

**Objective:** Measure and document real-world performance on physical hardware.

### Phase 23.1: Latency Benchmarking (2201–2240)

| Step | Title | Acceptance |
|------|-------|------------|
| 2201 | **Inspect — Latency components** | Audio capture, MFCC, inference, USB TX, host dispatch, ngspice, result return |
| 2202 | **Trace — Measurement methodology** | GPIO toggle (PTT) → oscilloscope; host timestamp (result); synchronized clocks |
| 2203 | **Specify — Benchmark protocol** | N ≥ 100 PTT cycles; controlled phrases; ambient noise < 40dB; 25°C |
| 2204 | **Implement — Latency harness** | `tools/latency_benchmark.py`: automates PTT, captures timestamps, computes stats |
| 2204 | **Test — Harness validation** | Known delay injection → measured within 1ms |
| 2205 | **Run — Latency benchmark** | 200 cycles × 3 runs (morning/afternoon/evening); record all component latencies |
| 2206 | **Run — Component breakdown** | Instrument each stage: capture, MFCC, inference, USB, host, simulation |
| 2207 | **Review — Latency report** | `docs/LATENCY_BENCHMARK_REPORT.md`: p50/p95/p99 per component, total |
| 2208 | **Document — Latency evidence** | `results/latency_benchmark.json` with `MEASURED` label |
| 2209 | **Integrate — Latency in evidence pack** | `docs/EVIDENCE_PACK.md` includes latency |
| 2210 | **Gate — Latency benchmarked** | N ≥ 200; all components measured; `MEASURED` evidence archived |

### Phase 23.2: Throughput & Resource Benchmarking (2211–2260)

| Step | Title | Acceptance |
|------|-------|------------|
| 2211 | **Inspect — Throughput metrics** | Max sustained PTT rate; audio sample rate stability; USB bandwidth utilization |
| 2212 | **Trace — Resource metrics** | CPU (per core), heap, stack, flash, SRAM, flash wear, temperature |
| 2213 | **Specify — Throughput protocol** | Max PTT frequency test: ramp rate until frame drops; sustained rate for 10 min |
| 2214 | **Implement — Throughput harness** | `tools/throughput_benchmark.py`: automated ramp, resource logging |
| 2214 | **Test — Throughput validation** | Known load → measured throughput within 5% |
| 2215 | **Run — Throughput benchmark** | Ramp test + 10 min sustained at max stable rate; log all resources |
| 2216 | **Run — Thermal soak** | 1 hour max throughput; log temperature, current, throttling events |
| 2217 | **Review — Throughput report** | `docs/THROUGHPUT_BENCHMARK_REPORT.md`: max rate, sustained rate, resource utilization |
| 2218 | **Document — Throughput evidence** | `results/throughput_benchmark.json` with `MEASURED` label |
| 2219 | **Integrate — Throughput in evidence pack** | `docs/EVIDENCE_PACK.md` includes throughput |
| 2220 | **Gate — Throughput benchmarked** | Max rate measured; sustained rate stable; thermal safe; `MEASURED` evidence |

### Phase 23.3: Accuracy & Quality Benchmarking (2221–2280)

| Step | Title | Acceptance |
|------|-------|------------|
| 2221 | **Inspect — Accuracy metrics** | Intent classification accuracy (on-device), simulation result correctness, VAD precision/recall |
| 2222 | **Trace — Test sets** | Held-out test speakers (from Phase 15); known-good simulation references |
| 2223 | **Specify — Accuracy protocol** | 500 intent utterances (test speakers); 50 simulation runs (known netlists) |
| 2224 | **Implement — Accuracy harness** | `tools/accuracy_benchmark.py`: automates utterance playback, simulation verification |
| 2224 | **Test — Harness validation** | Known inputs → measured accuracy within expected range |
| 2225 | **Run — Accuracy benchmark** | 500 utterances (test speakers) → on-device classification → confusion matrix |
| 2226 | **Run — Simulation correctness** | 50 ngspice runs → compare output to reference (SPICE gold standard) |
| 2227 | **Review — Accuracy report** | `docs/ACCURACY_BENCHMARK_REPORT.md`: intent acc, VAD P/R, sim correctness |
| 2228 | **Document — Accuracy evidence** | `results/accuracy_benchmark.json` with `MEASURED` label |
| 2229 | **Integrate — Accuracy in evidence pack** | `docs/EVIDENCE_PACK.md` includes accuracy |
| 2230 | **Gate — Accuracy benchmarked** | Intent acc > 90%; VAD P>95%/R>90%; sim correctness 100%; `MEASURED` evidence |

### Phase 23.4: Power & Efficiency Benchmarking (2231–2300)

| Step | Title | Acceptance |
|------|-------|------------|
| 2231 | **Inspect — Power domains** | MCU core, I2S, radio (off), flash, USB PHY, LDO efficiency |
| 2232 | **Trace — Measurement setup** | USB power meter (inline); MCU current via shunt; battery life projection |
| 2233 | **Specify — Power protocol** | Idle, listening, capturing, processing, transmitting; 10 min each; 3.3V/5V rails |
| 2234 | **Implement — Power harness** | `tools/power_benchmark.py`: controls power meter, logs per-state current |
| 2234 | **Test — Power meter validation** | Known load → measured within 2% |
| 2235 | **Run — Power benchmark** | 10 min per state × 3 runs; log current, voltage, power; compute battery life |
| 2235 | **Run — Battery life projection** | Typical usage profile (10 commands/hour, 8h/day) → projected days |
| 2236 | **Review — Power report** | `docs/POWER_BENCHMARK_REPORT.md`: per-state power, battery life, thermal |
| 2236 | **Document — Power evidence** | `results/power_benchmark.json` with `MEASURED` label |
| 2237 | **Integrate — Power in evidence pack** | `docs/EVIDENCE_PACK.md` includes power |
| 2238 | **Gate — Power benchmarked** | All states measured; battery life projected; `MEASURED` evidence archived |

---

## Phase 24 — End-to-End Prototype Demonstration (Steps 2301–2400)

**Objective:** Rehearsed, recorded, evidence-backed voice-to-action demonstration.

### Phase 24.1: Demo Script & Rehearsal (2301–2340)

| Step | Title | Acceptance |
|------|-------|------------|
| 2301 | **Inspect — Demo requirements** | Vishwakarma submission: 3-5 min video; live or recorded; specific scenarios |
| 2302 | **Trace — Demo scenarios** | Define: 3 core scenarios (open+simulate, context recall, error recovery) |
| 2303 | **Specify — Demo script** | Exact phrases, expected actions, timing, visual cues, backup plans |
| 2304 | **Implement — Demo automation** | `tools/demo_rehearsal.py`: runs full script, captures video + telemetry |
| 2304 | **Test — Dry run** | Execute script → verify all actions succeed, timing within limits |
| 2305 | **Run — Rehearsal sessions** | 10 full rehearsals; refine script, fix flaky steps |
| 2306 | **Review — Rehearsal report** | `docs/DEMO_REHEARSAL_REPORT.md`: success rate, timing, issues fixed |
| 2307 | **Document — Final demo script** | `docs/FINAL_DEMO_SCRIPT.md`: exact phrases, timing, camera angles |
| 2308 | **Integrate — Demo in Makefile** | `make hw-demo-record` target |
| 2309 | **Gate — Demo rehearsed** | 10 consecutive successful rehearsals; timing consistent |

### Phase 24.2: Evidence Capture (2311–2360)

| Step | Title | Acceptance |
|------|-------|------------|
| 2311 | **Inspect — Evidence requirements** | Video (1080p/30fps), screen recording, serial log, telemetry, photos |
| 2312 | **Trace — Capture setup** | Camera (tripod), screen recorder (OBS), serial logger, telemetry CSV |
| 2313 | **Specify — Evidence checklist** | 30 items: video, screen, serial, telemetry, photos, dataset card, model card |
| 2314 | **Implement — Evidence capture script** | `tools/capture_evidence.py`: starts all recorders, stops on demo complete |
| 2314 | **Test — Capture test** | Run script → all recorders start/stop correctly; files playable |
| 2315 | **Run — Recorded demo** | Execute `make hw-demo-record` → produces complete evidence set |
| 2316 | **Run — Backup recording** | Second camera angle; redundant serial logger |
| 2317 | **Review — Evidence quality** | Video: clear audio, visible actions; Screen: legible text; Serial: complete |
| 2318 | **Document — Evidence manifest** | `docs/EVIDENCE_MANIFEST.md`: file list, checksums, descriptions |
| 2319 | **Integrate — Evidence in submission** | `docs/SUBMISSION_EVIDENCE/` organized per checklist |
| 2320 | **Gate — Evidence captured** | All 30 items present; quality verified; manifest complete |

### Phase 24.3: Final Validation & Submission Prep (2321–2400)

| Step | Title | Acceptance |
|------|-------|------------|
| 2321 | **Inspect — Submission checklist** | `docs/SUBMISSION_CHECKLIST.md`: all items ticked |
| 2322 | **Trace — Final verification** | Deck matches implementation; evidence supports all claims; no TBD |
| 2323 | **Specify — Final gate criteria** | All 10 prototype acceptance gates (from workflow.md) have evidence |
| 2324 | **Implement — Final validator** | `tools/final_validator.py`: checks all gates, produces pass/fail report |
| 2324 | **Test — Final validation** | Run validator → all gates pass |
| 2325 | **Run — Final end-to-end test** | Cold boot → full demo → all gates pass |
| 2326 | **Review — Final validation report** | `docs/FINAL_VALIDATION_REPORT.md`: all gates, evidence refs |
| 2327 | **Document — Submission package** | `docs/SUBMISSION_PACKAGE.md`: deck, video, evidence, code tag |
| 2328 | **Integrate — Release tag** | `git tag -a v1.0.0-prototype -m "VaaniCore Prototype v1.0.0"` |
| 2329 | **Integrate — Submission upload** | Package uploaded to submission portal |
| 2330 | **Gate — Prototype accepted** | All acceptance gates pass; submission submitted; tag pushed |

---

## Phase 25 — Release Engineering & Final Documentation (Steps 2401–2500)

**Objective:** Production-ready installation, documentation, and handoff.

### Phase 25.1: Installation Packaging (2401–2440)

| Step | Title | Acceptance |
|------|-------|------------|
| 2401 | **Inspect — Install targets** | Linux (Ubuntu 22.04+, Fedora 38+), optional: macOS, Windows (WSL2) |
| 2402 | **Trace — Dependency graph** | Python deps, ESP-IDF, KiCad, ngspice, sounddevice, udev rules, dialout group |
| 2403 | **Specify — Installer design** | Bash script + Python; idempotent; `--user` or `--system`; uninstall support |
| 2404 | **Implement — Installer script** | `scripts/install.sh`: detects OS, installs deps, sets up venv, udev, dialout |
| 2404 | **Implement — Config generator** | `scripts/config_wizard.py`: interactive: serial port, project root, editor |
| 2405 | **Test — Clean install** | Fresh VM → run installer → `make test` passes |
| 2406 | **Run — Multi-distro test** | Ubuntu 22.04, Fedora 38, WSL2 Ubuntu → all pass |
| 2407 | **Review — Installer report** | `docs/INSTALLER_REPORT.md`: platforms, time, failure modes |
| 2408 | **Document — Installation guide** | `docs/INSTALLATION_GUIDE.md`: prerequisites, steps, troubleshooting |
| 2409 | **Integrate — Installer in repo** | `scripts/install.sh`; `make install` target |
| 2410 | **Gate — Installer production-ready** | Fresh install works on all target platforms |

### Phase 25.2: Operational Documentation (2411–2460)

| Step | Title | Acceptance |
|------|-------|------------|
| 2411 | **Inspect — Doc gaps** | Audit: README, INSTALLATION, USER_GUIDE, OPERATOR_RUNBOOK, DEVELOPER_GUIDE |
| 2412 | **Trace — Audience mapping** | End-user (demo), Operator (daily), Maintainer (debug), Developer (extend) |
| 2413 | **Specify — Documentation structure** | `/docs`: user/, operator/, maintainer/, developer/, reference/ |
| 2414 | **Implement — Operator runbook** | `docs/operator/RUNBOOK.md`: startup, demo, shutdown, common issues, contacts |
| 2414 | **Implement — Maintainer guide** | `docs/maintainer/GUIDE.md`: repo layout, build, test, debug, release process |
| 2415 | **Implement — Developer guide** | `docs/developer/GUIDE.md`: architecture, adding tools, tests, CI |
| 2415 | **Implement — Reference docs** | `docs/reference/`: API, protocols, schemas, configs |
| 2416 | **Test — Documentation accuracy** | Follow runbook → successful demo; follow maintainer guide → successful build |
| 2417 | **Run — Documentation review** | Peer review: clarity, completeness, accuracy |
| 2418 | **Document — Documentation index** | `docs/README.md` with navigation |
| 2419 | **Integrate — Docs in repo** | All under `docs/`; linked from main README |
| 2420 | **Gate — Documentation complete** | All audiences covered; accurate; reviewed |

### Phase 25.3: Release Engineering (2421–2480)

| Step | Title | Acceptance |
|------|-------|------------|
| 2421 | **Inspect — Release process** | Current: manual tag; Need: automated build, test, sign, package, publish |
| 2422 | **Trace — Release artifacts** | Source tarball, wheel, firmware binaries, installer, docs, SBOM |
| 2423 | **Specify — Release pipeline** | GitHub Actions: tag → build → test → sign → package → publish → GitHub Release |
| 2424 | **Implement — CI/CD pipeline** | `.github/workflows/release.yml`: matrix build, test, sign, upload |
| 2424 | **Implement — Signing** | GPG sign: source tarball, wheel, firmware; cosign for containers |
| 2425 | **Implement — SBOM generation** | `scripts/generate_sbom.py`: CycloneDX; all Python + C deps |
| 2425 | **Test — Release pipeline** | Push tag → workflow runs → artifacts uploaded to GitHub Release |
| 2426 | **Run — Release dry-run** | `git tag v1.0.0-rc1` → verify all artifacts |
| 2427 | **Review — Release report** | `docs/RELEASE_REPORT.md`: artifacts, signatures, SBOM, test results |
| 2427 | **Document — Release process** | `docs/RELEASE_PROCESS.md` |
| 2428 | **Integrate — Release automation** | `make release` target triggers workflow |
| 2429 | **Gate — Release engineering complete** | Pipeline produces signed, verified artifacts; SBOM valid |

### Phase 25.4: Handoff & Closure (2431–2500)

| Step | Title | Acceptance |
|------|-------|------------|
| 2431 | **Inspect — Handoff requirements** | Clean clone → install → demo → maintain; mentor sign-off |
| 2432 | **Trace — Handoff checklist** | `docs/HANDOFF_CHECKLIST.md`: repo access, credentials, docs, known issues |
| 2433 | **Specify — Handoff package** | Repo (with tags), credentials (encrypted), runbook, architecture decision log |
| 2434 | **Implement — Handoff package** | `scripts/create_handoff_package.py`: bundles repo, docs, credentials |
| 2434 | **Test — Clean handoff** | Fresh machine → extract package → install → demo → success |
| 2435 | **Run — Mentor handoff session** | Scheduled walkthrough; mentor signs `docs/MENTOR_SIGN_OFF.md` |
| 2436 | **Run — Team knowledge transfer** | Recorded walkthroughs: architecture, build, debug, extend |
| 2437 | **Review — Handoff completion** | `docs/HANDOFF_COMPLETION_REPORT.md`: all items complete |
| 2438 | **Document — Lessons learned** | `docs/LESSONS_LEARNED.md`: technical, process, team |
| 2439 | **Document — Project closure** | `docs/PROJECT_CLOSURE.md`: final status, future work, acknowledgments |
| 2440 | **Gate — Project complete** | Handoff package delivered; mentor signed; repo archived; project closed |

---

## Cross-Cutting Concerns (Apply to All Phases)

1. **Evidence Hygiene:** Every quantitative result labeled `MEASURED/SIMULATED/TARGET/ESTIMATED` with provenance.
2. **Regression Testing:** `make test`, `make sim-demo`, `make audit` after every modification.
3. **Commit Discipline:** Coherent milestones; descriptive messages; no evidence overwritten.
4. **Status Tracking:** `docs/WORKFLOW_STATUS.md` updated after every completed step.
5. **Security Invariants:** Allow-list, path jail, no-shell, confirm-gate, audit-log hold at all times.
6. **Hardware Consistency:** Pinmap.csv authoritative; schematic/PCB/firmware/docs aligned.
7. **Blockers Documented:** External dependencies explicitly recorded; independent work continues.
8. **No Fabrication:** Zero invented measurements, dataset samples, consent, prices, or sign-offs.

---

## Phase II Acceptance Gate (Step 2500)

The Phase II prototype is accepted only when **all** of the following have `MEASURED` evidence:

- [ ] ESP32-S3 firmware builds reproducibly with documented ESP-IDF version and flashes to identified board
- [ ] Physical PTT and mute controls behave as specified; microphone captures 16kHz audio with known format
- [ ] Trained, speaker-independent evaluated intent model runs on-device; accuracy > 90% on held-out speakers
- [ ] Device-to-host messages pass framing, CRC, sequence, ACK, and timeout checks over physical USB serial
- [ ] Host rejects unknown commands and out-of-project paths; no arbitrary shell execution possible
- [ ] Supported voice command opens local electronics project, runs ngspice, verifies result
- [ ] Follow-up context query retrieves persisted project/task event after host restart
- [ ] Disconnect, malformed frame, timeout, host restart, and denied-action cases have recorded outcomes
- [ ] Dashboard shows actual device/agent/execution state; virtual data labeled `SIMULATED`
- [ ] KiCad ERC/DRC, pin compatibility, power review, and fabrication outputs reviewed before board order
- [ ] Evidence package distinguishes targets, estimates, simulated results, and physical measurements
- [ ] Presentation and README claims match implementation state at release commit

---

## Appendix: Step ID Allocation Summary

| Phase | Steps | Range | Primary Deliverable |
|-------|-------|-------|---------------------|
| 11 | 100 | 1001–1100 | Audit baseline, ground-truth matrix, toolchain validation |
| 12 | 100 | 1101–1200 | Compilable, flashable ESP32-S3 firmware |
| 13 | 100 | 1201–1300 | ERC/DRC clean KiCad schematic, PCB, BOM, fab package |
| 14 | 100 | 1301–1400 | Validated I2S/GDMA/DSP/VAD audio pipeline on hardware |
| 15 | 100 | 1401–1500 | 3-speaker consented dataset with speaker-split |
| 16 | 100 | 1501–1600 | Trained, evaluated, quantized DS-CNN on device |
| 17 | 100 | 1601–1700 | Physical voice-to-action demo with MEASURED evidence |
| 18 | 100 | 1701–1800 | Local LLM + planner + memory + guardrails |
| 19 | 100 | 1801–1900 | Tool registry, approval gates, executor, GUI |
| 20 | 100 | 1901–2000 | Vector memory, semantic resolver, task recovery, context-aware planning |
| 21 | 100 | 2001–2100 | Real-time telemetry dashboard with alerts and history |
| 22 | 100 | 2101–2200 | Fault injection, signed firmware, self-healing, tamper-evident audit |
| 23 | 100 | 2201–2300 | Latency, throughput, accuracy, power benchmarks (MEASURED) |
| 24 | 100 | 2301–2400 | Rehearsed, recorded, evidence-backed demonstration |
| 25 | 100 | 2401–2500 | Installer, docs, release automation, handoff package |

**Total Phase II Steps: 1,500 (1001–2500)**