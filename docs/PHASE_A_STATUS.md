# Phase-A evidence matrix

| Requirement | Evidence | Status |
|---|---|---|
| Python/C protocol + CRC16 vectors | `make protocol-test`, `tests/protocol/vectors.json` | VERIFIED_HOST_COMPILED |
| ACK/NACK/retry policy | `host/session.py`, `host/reliability.py`, unit tests | VERIFIED_SOFTWARE |
| Allow-list/path jail/no shell | `host/host_agent.py`, security tests | VERIFIED_HOST |
| Virtual intent → host action loop | `make sim-demo` including `host_agent.py --stdio --virtual` | VERIFIED_SIMULATED |
| TIME_SYNC/PROJECT_EVENT lifecycle | `host/session.py`, session tests | VERIFIED_SOFTWARE |
| LAST/YESTERDAY context | Python and C context tests | VERIFIED_HOST_COMPILED |
| MFCC Python/C parity | `make dsp-test`, max error 0.0139313 | VERIFIED_HOST_COMPILED |
| I2S/GDMA/RTOS firmware | `firmware/main/` source scaffold | WRITTEN_NOT_BUILT — `[[HUMAN: install ESP-IDF and build]]` |
| TFLite-Micro int8 classifier | `ml/model.py`, gated training and int8 export paths | BLOCKED_INPUT/TOOLCHAIN — `[[HUMAN: record/train/export model]]` |
| Human audio capture tool | `tools/record_dataset.py --help`; backend-gated WAV/metadata writer | VERIFIED_TOOLING_ONLY — microphone and `sounddevice` still required |
| OLED/physical buttons/LEDs | GPIO scaffold; OLED absent | PARTIAL — `[[HUMAN: wire and validate hardware]]` |
| N≥30 benchmark harness | `results/virtual_trials.csv`, 30 rows | VERIFIED_SIMULATED_ONLY |
| Real P1/P2/P3 measurements | no hardware result files | BLOCKED_HUMAN_HARDWARE |
| Official-template draft deck | `deck/out/Vishwakarma_Stage2_VaaniCore.pptx` | VERIFIED_STRUCTURE; visual QA required |
| Final deck | placeholders remain | BLOCKED_HUMAN_METADATA/EVIDENCE |
| CAD/KiCad native artifacts | README and analytical estimate only | BLOCKED_HUMAN_DESIGN_WORK |
| Verified citations/prices/photos/sign-offs | placeholders remain | BLOCKED_HUMAN_EVIDENCE |

This matrix is a status record, not a claim that Phase A is complete.
