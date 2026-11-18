# Speaker-Split Dataset Specification

**Generated:** 2026-11-19T04:05:00Z
**Git Commit:** c394453
**Status:** APPROVED (spec complete, dataset BLOCKED on recording)

---

## Contract

**Scope:** Speaker-isolated dataset for intent classification training and evaluation.

**Purpose:** Ensure no speaker leakage between train/validation/test splits.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Speakers | 3 (minimum) |
| Clips per speaker | 480 (16 per class × 13 classes × 3 speakers = 1440) |
| Duration per clip | 2.0 seconds |
| Sample rate | 16 kHz |
| Format | 16-bit PCM WAV, mono |
| Split method | By speaker_id (not by sample) |
| Train/Val/Test | 70% / 15% / 15% of speakers |

---

## Data Structure

```
dataset/
├── metadata.jsonl          # All samples metadata
├── open_amplifier/
│   ├── speaker1_001.wav
│   ├── speaker1_002.wav
│   ├── speaker2_001.wav
│   └── ...
├── open_filter/
│   └── ...
└── ... (13 class directories)
```

### Metadata JSONL Schema
```json
{
  "class": "open_amplifier",
  "filepath": "dataset/open_amplifier/speaker1_001.wav",
  "duration": 2.0,
  "sample_rate": 16000,
  "speaker_id": "speaker1",
  "timestamp": "2026-11-19T14:30:22.123456"
}
```

---

## Split Algorithm (`ml/dataset.py`)

```python
def speaker_split(metadata: list[dict], train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    # 1. Group by speaker_id
    speakers = defaultdict(list)
    for entry in metadata:
        speakers[entry["speaker_id"]].append(entry)
    
    # 2. Shuffle speaker IDs
    speaker_ids = list(speakers.keys())
    random.shuffle(speaker_ids)
    
    # 3. Split speakers
    n_train = int(len(speaker_ids) * train_ratio)
    n_val = int(len(speaker_ids) * val_ratio)
    
    train_speakers = set(speaker_ids[:n_train])
    val_speakers = set(speaker_ids[n_train:n_train+n_val])
    test_speakers = set(speaker_ids[n_train+n_val:])
    
    # 4. Assign samples
    train = [e for e in metadata if e["speaker_id"] in train_speakers]
    val = [e for e in metadata if e["speaker_id"] in val_speakers]
    test = [e for e in metadata if e["speaker_id"] in test_speakers]
    
    return train, val, test
```

---

## Invariants

1. **No speaker crossover** — Same speaker_id never in multiple splits
2. **Class balance per speaker** — Each speaker records all 13 classes
3. **Consent per speaker** — Explicit agreement before recording
4. **Minimum 3 speakers** — Required for leave-one-speaker-out eval
5. **480 clips/speaker** — 16 per class (13 classes + some extra for _silence_)
6. **16kHz 16-bit mono** — Matches firmware I2S capture

---

## Target Collection (TODO_HUMAN.md Day 4)

| Speaker | Classes | Clips/Class | Total Clips |
|---------|---------|-------------|-------------|
| speaker1 | 13 | ~37 | 480 |
| speaker2 | 13 | ~37 | 480 |
| speaker3 | 13 | ~37 | 480 |
| **Total** | | | **1440** |

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_speakers_never_cross_split` | No speaker_id in multiple splits |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| < 3 speakers | Leave-one-speaker-out eval impossible |
| Speaker imbalance | Stratified split by speaker (not implemented) |
| Missing class for speaker | Model cannot learn that class for that speaker |
| Consent not obtained | Data unusable (ethical/legal) |

---

## Acceptance Criteria

- Speaker-split algorithm specified
- Metadata schema defined
- Target collection numbers (3 speakers, 480 clips each)
- Invariants: no crossover, class balance, consent, min 3 speakers
- Dataset BLOCKED on recording (sounddevice, microphone, consent)
- Next step (0364) can use this output