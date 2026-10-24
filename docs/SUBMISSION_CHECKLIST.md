# VaaniCore Stage-2 submission checklist — draft

This is a live checklist. A checked software item means the repository contains the artifact and its automated check passed; it does not mean hardware validation occurred.

## Verified in this workspace

- [x] Official template PPTX and idea PDF are present under `inputs/`.
- [x] Python protocol, CRC, retry, malformed-frame, and fuzz tests pass.
- [x] C protocol, context, intent, and MFCC parity tests pass.
- [x] Virtual device → host allow-list → simulation-status loop passes.
- [x] `shell=True` security check and project path-jail tests pass.
- [x] Draft deck archive has 18 active slides and structural QA passes.
- [x] Benchmark artifacts are explicitly labelled `SIMULATED`, not hardware evidence.
- [x] Pin-map, power-budget, FMEA, and analytical enclosure checks generate provenance-bearing artifacts.

## Required before final submission

- [ ] Install ESP-IDF v5.x; build, flash, and test the ESP32-S3 firmware.
- [ ] Record the three-speaker dataset; train/export/evaluate the int8 model with leave-one-speaker-out splits.
- [ ] Collect real P1/P2/P3 latency, CPU/RAM, USB traffic, power, reliability, and timing-study data.
- [ ] Draw and review the KiCad schematic/layout; commit native `.kicad_sch` and `.kicad_pcb` files.
- [ ] Generate and inspect native STEP/STL files; add real renders and fit evidence.
- [ ] Verify BOM vendors, prices, and lead times; retain source evidence.
- [ ] Add application ID, institution, track, mentor, repository URL, photos, and sign-offs.
- [ ] Render every deck slide in PowerPoint/LibreOffice and fix visual overflow/overlap.
- [ ] Replace all `[[HUMAN: ...]]` placeholders, then run `make deck-final`.

## Final commands

```sh
make test
make sim-demo
make bench
make audit
make hardware-check
make deck-final
```

`make deck-final` is intentionally expected to fail until the human-only evidence above is supplied.
