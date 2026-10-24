# Human task list

- [x] Add the official template PPTX and idea PDF under `inputs/` (verified present in this workspace).
- [ ] Supply application ID, institution, track, mentor, repository URL, and actual Stage-2 deadline.
- [ ] Install ESP-IDF v5.x and build/flash the firmware on two ESP32-S3 boards.
- [ ] Record the 3-speaker dataset and run the leave-one-speaker-out ML evaluation.
- [ ] Capture hardware measurements, timing-study CSV, ID-badge photos, and mentor sign-off.
- [ ] Verify India vendor prices/lead times and replace all BOM placeholders.

## 14-day execution checklist

| Day | Human action | Run afterwards | Refresh |
|---|---|---|---|
| 1 | Install ESP-IDF, order/collect parts, provide deadline and application metadata | `idf.py build` | S1, S7, S11 |
| 2 | Wire mic and capture a WAV over I2S/DMA | firmware capture test | S6, S10 |
| 3 | Flash CDC echo and connect host | `make sim-demo` plus serial smoke test | S6, S13 |
| 4 | Each member records 480 labelled clips with `tools/record_dataset.py` | ML metadata validator | S15, S16 |
| 5 | Train/export int8 model and flash it | ML eval and device inference test | S7, S15 |
| 6 | Run first physical PTT-to-simulation demo; capture 3 photos and one screen recording | evidence log and serial transcript | S4, S5, S12 |
| 7 | Exercise LAST/YESTERDAY with 20 scripted cases | context test | S6, S15, S16 |
| 8 | Run VAD/wake test; choose wake fallback if needed | false-accept report | S15, S16 |
| 9 | Test confirm, unplug, garbage frames, host crash, watchdog | FMEA test matrix | S13, S16 |
| 10 | Run P1/P2/P3 dry-run and install power instrument | `make bench` | S5, S15 |
| 11 | Collect N≥30 measurements per condition and timing study | analysis scripts | S4, S5, S15 |
| 12 | Draw KiCad schematic/layout and CAD enclosure; export native files | ERC/DRC and CAD checks | S8, S9, S10, S11 |
| 13 | Add evidence photos, verified citations and deck metadata; rehearse | `make deck-draft` then visual QA | all slides |
| 14 | Freeze, bug-fix only, obtain mentor review, submit and tag | `make deck-final` | submission package |

Day-specific work is blocked until the hardware and official inputs are supplied; no measurements are inferred.
