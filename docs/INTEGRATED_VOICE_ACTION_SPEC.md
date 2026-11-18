# Integrated Voice-to-Action Specification

**Generated:** 2026-11-19T05:35:00Z
**Git Commit:** ae74c9b
**Status:** APPROVED (virtual complete, physical BLOCKED)

---

## Contract

**Scope:** End-to-end voice command to simulation result flow.

**Purpose:** Define the complete integrated pipeline for the narrow demo.

---

## Narrow Demo Scenario

**Voice Command:** "Open the amplifier project and run the simulation"

**Supported Variants:**
- "Run simulation on amplifier"
- "Amplifier run simulation"
- "Open amplifier and run simulation"

---

## Complete Flow (Virtual - Working)

```
User speaks phrase
       ↓
Virtual Device: phrase_to_frame() → Frame(RUN_SIMULATION, {project: amplifier, open: 1})
       ↓
Host Session: connect_frames() → TIME_SYNC (seq=1)
       ↓
Host Session: handle(RUN_SIMULATION) → dispatch()
       ↓
Host Dispatch: _project("amplifier") → path jail check → launch_project() (xdg-open)
       ↓
Host Dispatch: virtual=True → returns SIMULATED (gain_db=TARGET, bw_hz=TARGET, label=SIMULATED)
       ↓
Host Session: caches last_result, emits PROJECT_EVENT
       ↓
Host Returns: ACK + DONE + PROJECT_EVENT
       ↓
Virtual Device: device.handle() → context updated (local_day, history)
       ↓
User: "Show result" → SHOW_RESULT → cached last_result returned
```

**Frame Sequence (20 frames):**
1. Host→Device: TIME_SYNC (seq=1)
2. Device→Host: ACK (seq=1)
3. Device→Host: DONE (seq=1)
4. Device→Host: PING (seq=1)
5. Host→Device: ACK (seq=1)
6. Host→Device: DONE (seq=1)
7. Device→Host: RUN_SIMULATION (seq=2, project=amplifier, open=1)
8. Host→Device: ACK (seq=2)
9. Host→Device: DONE (seq=2, SIMULATED, opened=1)
10. Host→Device: PROJECT_EVENT (seq=2)
11. Device→Host: SHOW_RESULT (seq=3)
12. Host→Device: ACK (seq=3)
13. Host→Device: DONE (seq=3, cached)
14. Device→Host: RUN_SIMULATION (seq=4, project=amplifier)
15. Host→Device: ACK (seq=4)
16. Host→Device: DONE (seq=4, SIMULATED)
17. Host→Device: PROJECT_EVENT (seq=4)
18. Device→Host: SHOW_RESULT (seq=5)
19. Host→Device: ACK (seq=5)
20. Host→Device: DONE (seq=5, cached)

---

## Complete Flow (Physical - BLOCKED)

```
User presses PTT (GPIO15)
       ↓
Firmware: audio_task captures 16kHz mono via I2S/GDMA (256 samples/frame)
       ↓
Firmware: dsp_task computes MFCC (10 coeffs) from audio frames
       ↓
Firmware: infer_task runs TFLite-Micro int8 on MFCC → class_name
       ↓
Firmware: intent_task looks up class_name → vc_intent_t → builds frame
       ↓
Firmware: comms_task sends frame via USB CDC (TinyUSB)
       ↓
Host: transport.py receive → decode → session.handle → dispatch
       ↓
Host: action (launch project, run ngspice) → response frames
       ↓
Host: USB CDC send → Firmware receive → decode → context update → LED status
```

---

## Blockers for Physical Integration

| Blocker | Phase | Status |
|---------|-------|--------|
| ESP-IDF not installed | 5.1 | BLOCKED |
| Firmware not built/flashed | 5.1 | BLOCKED |
| Audio hardware not connected | 5.2 | BLOCKED |
| Dataset not recorded | 6.1 | BLOCKED |
| Model not trained/exported | 6.3-6.4 | BLOCKED |
| ngspice not installed | 2.x | BLOCKED |

---

## Invariants

1. **Virtual = physical protocol** — Same frames, same CRC, same sequencing
2. **SIMULATED label explicit** — Virtual mode never claims MEASURED
3. **Path jail enforced** — Host never executes arbitrary paths
4. **Allow-list only** — Only 5 verbs cross boundary
5. **Context sync** — PROJECT_EVENT updates both host and device
6. **PTT is trigger** — Physical button starts capture (no wake word in MVP)

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `make sim-demo` | Virtual flow complete (20 frames) |
| `make test` | All components individually tested |

---

## Failure Modes

| Condition | Virtual Behavior | Physical Behavior |
|-----------|------------------|-------------------|
| Unknown phrase | ERR:unrecognised_intent | Device sends ERR frame |
| ngspice missing | N/A (virtual) | ERR:ngspice_unavailable |
| Hardware fault | N/A | ERR LED, NACK retry |
| Context loss | N/A | NVS recovers on boot |

---

## Acceptance Criteria

- Virtual flow fully specified (20 frames)
- Physical flow architecture defined
- 6 blockers identified
- 6 invariants enumerated
- Physical integration BLOCKED on hardware/ESP-IDF/dataset
- Next step (0514) can use this output