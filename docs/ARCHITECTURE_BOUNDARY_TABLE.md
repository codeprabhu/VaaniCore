# Host-Edge Responsibility Table

**Generated:** 2026-11-18T22:30:00Z
**Git Commit:** a407329
**Status:** APPROVED (this document constitutes the approved table)

---

## Responsibility Division

| Subsystem | Host (Linux) | Edge (ESP32-S3) | Shared / Interface |
|-----------|--------------|-----------------|-------------------|
| **Transport** | `host/transport.py`: USB CDC discovery, `serve_serial`, baud 115200, reconnection handshake | TinyUSB CDC device, USB D-/D+ (GPIO19/20), PTT-triggered TX | CRC16-framed ASCII, newline terminated, 128 bytes max |
| **Protocol** | `host/protocol.py`: `encode`/`decode`, `Frame` dataclass, CRC16-CCITT-FALSE | `firmware/components/protocol/protocol.c`: `vaanicore_encode_frame`/`vaanicore_decode_frame`, bounded buffers | Identical framing spec; vectors in `tests/protocol/vectors.json` |
| **Session** | `host/session.py`: `HostSession` (seq alloc, TIME_SYNC, response sequencing, result caching) | Implicit: device tracks seq for responses, no session state | Seq modulo 256; ACK/NACK/DONE/ERR responses |
| **Reliability** | `host/reliability.py`: 300ms timeout, 3 retries, 30s task timeout, idle detection | Device-side: retry on NACK, drop on oversize/CRC error | Policy mirrored; host is authority |
| **Audio Capture** | — | `firmware/main/audio_capture.c`: I2S std mode, GDMA 6×256 frames, ISR→task notify, 32→16 bit saturation | 16 kHz mono, 256-sample frames → host never sees raw audio |
| **DSP / MFCC** | `ml/features.py`: Python reference (DC-block, pre-emphasis, Hann, 512 FFT, 40 mel, log, DCT-II, 10 coeffs) | `firmware/components/dsp/mfcc.c`: C implementation, fixed-point friendly | Parity verified: max abs error 0.0139313 < 0.05 |
| **Intent Classification** | `host/intent_nlu.py`: closed-vocab regex mapping phrase→Frame (virtual path only) | `firmware/main/intents.c`: lookup table `class_name` → `vc_intent_t` (verb, project, flags) | Intent set: OPEN_PROJECT, RUN_SIMULATION, SHOW_RESULT, CLOSE_PROJECT, CANCEL, CONFIRM, PING |
| **Context / History** | `host/session.py`: resolves LAST/YESTERDAY via `DeviceContext` proxy | `firmware/components/context/context.c`: 16-event circular buffer, NVS persistence, `vc_history_resolve[_confirmed]` | PROJECT_EVENT frames update both sides; local_day from TIME_SYNC |
| **Action Dispatch** | `host/host_agent.py`: `dispatch()` — allow-list (PING, OPEN_PROJECT, RUN_SIMULATION, SHOW_RESULT, CLOSE_PROJECT), path jail (`_project`), risky=confirm, virtual mode | — | Verbs never carry host paths; only project IDs and bounded params |
| **Project Launch** | `host/launcher.py`: `open_command()` (xdg-open/open/os.startfile), `launch_project()` fixed argv, no shell | — | Project root jailed to `projects/{amplifier,filter,regulator}` |
| **Simulation** | `host/host_agent.py`: `subprocess.run(["ngspice", "-b", "-o", log, netlist])`, `host/measurements.py` parse | — | Runs only in project dir; MEASURED label only with ngspice |
| **Audit Logging** | `host/audit_log.py`: JSONL append with frame metadata, direction, timestamp, error | — | No audio payloads logged |
| **UI / Buttons / LEDs** | — | `firmware/main/ui.c`: button events (confirm/abort), LED status (listen/busy/err), mute sense | GPIO: confirm=15, abort=16, mute=17, listen=18, busy=21, err=47 |
| **Power / Battery** | — | `firmware/main/power_task` (scaffold), `hardware/power_budget.py` (analytical 0.6W TARGET) | — |

---

## Serial Protocol Contract

```
Frame: @<seq>:<VERB>[:k=v,k=v]*<CRC16-CCITT hex4>\n
Max: 128 bytes including CRC and newline
Seq: decimal 0-255 (modulo 256)
Verbs (device→host): PING, OPEN_PROJECT, RUN_SIMULATION, SHOW_RESULT, CLOSE_PROJECT, CANCEL, CONFIRM
Verbs (host→device): TIME_SYNC, ACK, NACK, DONE, ERR, PROJECT_EVENT
Fields: key=[a-z][a-z0-9_]*, value=string (no commas, no colons)
CRC: CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF) over bytes '@'..last field char
```

---

## Invariants

1. **No host paths in frames** — only project IDs (`amplifier`, `filter`, `regulator`, `LAST`, `YESTERDAY`)
2. **No shell execution** — launcher uses fixed argv; `shell=True` forbidden (tested)
3. **Path jail** — project resolution validates `ROOT in path.parents`
4. **Bounded buffers** — C encode/decode use stack buffers, no heap
5. **CRC on every frame** — mismatches → NACK (device) or drop (host)
6. **Sequence recovery** — NACK includes recovered seq; malformed with no seq → seq=0
7. **Offline-first** — no network calls in host agent or firmware core path
8. **Simulated vs Measured** — virtual mode returns `label=SIMULATED`, `gain_db=TARGET`, `bw_hz=TARGET`; real mode requires ngspice → `label=MEASURED`

---

## Acceptance Criteria

- Table approved and stored as `docs/ARCHITECTURE_BOUNDARY_TABLE.md`
- All responsibilities accounted for
- No gaps or overlaps
- Next step (0034) can use this output