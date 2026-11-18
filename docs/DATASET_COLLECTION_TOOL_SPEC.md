# Dataset Collection Tool Specification

**Generated:** 2026-11-19T03:55:00Z
**Git Commit:** c394453
**Status:** APPROVED (tool scaffolded, hardware BLOCKED)

---

## Contract

**Scope:** Audio dataset recording tool for consented speaker data.

**Purpose:** Enable collection of labeled intent utterances with speaker metadata.

---

## Tool: `tools/record_dataset.py`

### Usage
```bash
python3 tools/record_dataset.py --class open_amplifier --duration 2.0 --speaker speaker1 --output-dir dataset
```

### Arguments
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--class` | Yes | — | Intent class (from classes.json) |
| `--duration` | No | 2.0 | Recording duration (seconds) |
| `--sample-rate` | No | 16000 | Sample rate (Hz) |
| `--speaker` | Yes | — | Speaker identifier |
| `--output-dir` | No | dataset | Output directory |
| `--device` | No | default | sounddevice input device index |

---

## Output Format

### Audio Files
```
dataset/
└── open_amplifier/
    ├── 20261119_143022_speaker1.wav
    ├── 20261119_143045_speaker1.wav
    └── ...
```

### Metadata (JSONL)
```jsonl
{"class": "open_amplifier", "filepath": "dataset/open_amplifier/20261119_143022_speaker1.wav", "duration": 2.0, "sample_rate": 16000, "speaker_id": "speaker1", "timestamp": "2026-11-19T14:30:22.123456"}
{"class": "open_amplifier", "filepath": "dataset/open_amplifier/20261119_143045_speaker1.wav", "duration": 2.0, "sample_rate": 16000, "speaker_id": "speaker1", "timestamp": "2026-11-19T14:30:45.678901"}
```

---

## Intent Classes (`ml/configs/classes.json`)

```json
[
  "open_amplifier",
  "open_filter",
  "open_regulator",
  "open_last",
  "open_yesterday",
  "run_sim",
  "open_amp_run_sim",
  "open_yday_run_sim",
  "show_result",
  "cancel",
  "confirm",
  "close_project",
  "_silence_"
]
```

13 classes matching firmware intent table.

---

## Implementation (`record_dataset.py`)

```python
def record_dataset(class_name, duration, speaker_id, output_dir, sample_rate=16000):
    # 1. Validate class_name in classes.json
    # 2. Open sounddevice InputStream (mono, sample_rate)
    # 3. Record for duration seconds
    # 4. Save as WAV (16-bit PCM)
    # 5. Append metadata line to metadata.jsonl
```

---

## Dataset Loading (`ml/dataset.py`)

### Speaker-Split
- **Critical:** No speaker appears in both train and test
- Split by `speaker_id` metadata field
- Typical: 70% train, 15% val, 15% test speakers

### Feature Extraction
- Uses `ml/features.py` (MFCC pipeline)
- Output: (num_samples, num_frames, 10) for each sample

---

## Invariants

1. **Consent required** — Human must explicitly agree before recording
2. **Speaker isolation** — Train/val/test split by speaker_id, no overlap
3. **Class validation** — Only classes from classes.json accepted
4. **Metadata completeness** — Every WAV has JSONL entry
5. **Sample rate fixed** — 16kHz for DSP parity
4. **16-bit PCM WAV** — Compatible with firmware I2S capture
5. **Timestamped** — Filename and metadata include timestamp
6. **Tooling only** — No ML training in this tool

---

## Test Coverage

| Test | Status |
|------|--------|
| `test_speakers_never_cross_split` | ✅ PASS (ml/dataset.py) |
| `test_module_exists_and_help_contract_is_documented` | ✅ PASS |
| Audio recording | ❌ BLOCKED (requires sounddevice + microphone) |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| sounddevice not installed | ImportError, clear message |
| No microphone | sounddevice error |
| Invalid class | Validation error, exits |
| Disk full | OSError, partial save |
| Permission denied | OSError on output dir |

---

## Acceptance Criteria

- Tool interface specified with all arguments
- Output format (WAV + JSONL) defined
- Intent classes listed (13)
- Speaker-split requirement explicit
- 6 invariants enumerated
- Hardware dependencies BLOCKED (sounddevice, microphone)
- Next step (0354) can use this output