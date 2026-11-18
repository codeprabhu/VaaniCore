# Versioned Toolchain Manifest

**Generated:** 2026-11-18T23:00:00Z
**Git Commit:** a407329

---

## Python Environment

| Package | Version Constraint | Purpose | Status |
|---------|-------------------|---------|--------|
| python | 3.11+ | All host code, tests, ML, bench, deck, tools | ✓ Available |
| pyyaml | >=6.0 | Config parsing (config.yaml, projects.yaml, allowlist.yaml) | ✓ In requirements-dev.txt |
| numpy | >=1.24 | DSP, ML, benchmark analysis | ✓ In requirements-dev.txt |
| scipy | >=1.10 | DSP (FFT, mel filters), ML | ✓ In requirements-dev.txt |
| matplotlib | >=3.7 | Benchmark figures, timing analysis | ✓ In requirements-dev.txt |
| lxml | >=4.9 | Deck OOXML editing (python-pptx alternative) | ✓ In requirements-dev.txt |
| pytest | >=7.4 | Test runner (alternative to unittest) | ✓ In requirements-dev.txt |
| cadquery | >=2.4 | Parametric enclosure CAD | ✓ In requirements-dev.txt |
| sounddevice | >=0.4 | Audio capture for dataset recording | ✗ NOT INSTALLED (hardware blocked) |

**requirements-dev.txt content:**
```
pyyaml>=6.0
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
lxml>=4.9
pytest>=7.4
cadquery>=2.4
sounddevice>=0.4
```

---

## C Toolchain (Host Tests)

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| gcc | 11+ | Compile C test drivers (protocol, context, DSP, intent) | ✓ Available |
| make | 4.3+ | Build orchestration | ✓ Available |

**Test compilation flags:** `-std=c11 -O2 -I<component_include>`

---

## ESP-IDF Toolchain (Firmware Build)

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| ESP-IDF | v5.x (exact patch `[[HUMAN: pin after toolchain install]]`) | Firmware build for ESP32-S3 | ✗ NOT INSTALLED |
| xtensa-esp32s3-elf-gcc | IDF-bundled | Cross-compile firmware | ✗ NOT INSTALLED |
| esptool.py | IDF-bundled | Flash firmware | ✗ NOT INSTALLED |
| idf.py | IDF-bundled | Build system | ✗ NOT INSTALLED |

**Required command after install:**
```bash
idf.py set-target esp32s3 && idf.py build
```

**firmware/sdkconfig.defaults** exists with ESP32-S3 config.

---

## EDA Tools

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| KiCad | 8.0+ | Schematic capture, PCB layout, ERC/DRC, netlist export | ✗ NOT VERIFIED |
| ngspice | 40+ | SPICE simulation for MEASURED results | ✗ NOT INSTALLED |

---

## Deck Generation

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| python-pptx | N/A | Official template editing | ✗ UNAVAILABLE (sandbox) |
| lxml | >=4.9 | OOXML direct manipulation (current implementation) | ✓ IN USE |

**Decision (2026-10-24):** Use lxml to edit template OOXML directly since python-pptx unavailable in sandbox. Visual rendering requires human QA in PowerPoint/LibreOffice.

---

## Audio Capture

| Tool | Version | Purpose | Status |
|------|---------|---------|--------|
| sounddevice | >=0.4 | `tools/record_dataset.py` microphone input | ✗ NOT INSTALLED |
| PortAudio | System | sounddevice backend | ✗ NOT VERIFIED |

---

## CI Environment (GitHub Actions)

Per README.md:
- Installs `requirements-dev.txt`
- Runs `make test`, `make sim-demo`, `make bench`, `make audit`, `make deck-draft`
- ESP-IDF, ngspice, KiCad, sounddevice NOT in CI (hardware/blocked steps)

---

## Version Pinning Status

| Component | Pinned? | Notes |
|-----------|---------|-------|
| Python deps | In requirements-dev.txt | Loose constraints (>=) |
| ESP-IDF | `[[HUMAN: pin after toolchain install]]` | Decision #7 |
| KiCad | 8.0+ | `hardware/kicad/README.md` |
| ngspice | 40+ | Implicit |

---

## Acceptance Criteria

- Manifest documents all tools with versions and status
- Blocked/missing tools explicitly identified
- Next step (0064) can use this output