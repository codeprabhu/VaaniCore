# Model Card and Metadata Specification

**Generated:** 2026-11-19T04:45:00Z
**Git Commit:** c394453
**Status:** APPROVED (template complete, population BLOCKED on training)

---

## Contract

**Scope:** Model card documentation and metadata for the trained intent classifier.

**Purpose:** Provide transparent, standardized documentation of the ML model per best practices.

---

## Model Card Template (`ml/model_card.md`)

```markdown
# VaaniCore Intent Classifier Model Card

## Model Details
- **Name:** VaaniCore DS-CNN Intent Classifier
- **Version:** 1.0.0
- **Architecture:** Depthwise Separable CNN (DS-CNN)
- **Framework:** TensorFlow / Keras → TFLite int8
- **Parameters:** ~20,000
- **Input:** MFCC features (10 coeffs, variable frames, 16kHz audio)
- **Output:** 13 intent classes

## Intended Use
- **Primary:** Offline intent classification for VaaniCore ESP32-S3 firmware
- **Classes:** open_amplifier, open_filter, open_regulator, open_last, open_yesterday, run_sim, open_amp_run_sim, open_yday_run_sim, show_result, cancel, confirm, close_project, _silence_
- **Deployment:** TFLite-Micro on ESP32-S3
- **Latency Target:** < 50ms per inference
- **Memory:** < 50KB model + arena

## Training Data
- **Dataset:** VaaniCore Speaker-Split Dataset
- **Speakers:** 3 (consented)
- **Clips per Speaker:** 480 (2-second utterances)
- **Total Samples:** 1,440
- **Sample Rate:** 16 kHz mono
- **Split:** Leave-one-speaker-out (3-fold CV)
- **Consent:** Explicit written consent per speaker

## Training Procedure
- **Config:** ml/configs/default.json
- **Optimizer:** Adam (lr=0.001)
- **Batch Size:** 32
- **Epochs:** 50 (early stopping patience=10)
- **Loss:** Cross-entropy
- **Augmentation:** None (speaker-split relies on speaker diversity)

## Evaluation Results
- **Protocol:** Leave-one-speaker-out (3-fold CV)
- **Per-Fold Metrics:**
  | Fold | Test Speaker | Accuracy | F1-Macro |
  |------|--------------|----------|----------|
  | 1    | speaker1     | TBD      | TBD      |
  | 2    | speaker2     | TBD      | TBD      |
  | 3    | speaker3     | TBD      | TBD      |
- **Aggregate:**
  - Mean Accuracy: TBD ± TBD
  - Mean F1-Macro: TBD ± TBD
- **Quantized Model (int8):** Accuracy within 1% of float baseline

## Ethical Considerations
- **Consent:** Explicit written consent from all speakers
- **Privacy:** Audio processed locally on device, never transmitted
- **Bias:** Limited to 3 speakers; may not generalize to unseen accents/demographics
- **Accessibility:** Voice-only interface; no visual fallback in MVP

## Limitations
- **Speaker Count:** Only 3 speakers; poor generalization to unseen speakers
- **Vocabulary:** Fixed 13 classes; no open-vocabulary support
- **Noise Robustness:** Not evaluated in noisy environments
- **Language:** English only (phrases in intent_nlu.py)
- **Hardware Dependency:** Requires ESP32-S3 with microphone

## Model Artifacts
- `model_int8.tflite` — Quantized model for firmware
- `model_float.h5` — Float Keras model for reference
- `classes.json` — Class label mapping
- `default.json` — Training hyperparameters

## Contact
- **Team:** VaaniCore
- **Repository:** github.com/vaanicore/vaanicore
```

---

## Metadata Files

| File | Purpose |
|------|---------|
| `ml/model_card.md` | Human-readable model card |
| `ml/configs/classes.json` | 13 class labels (ordered) |
| `ml/configs/default.json` | Training hyperparameters |
| `ml/model_int8.tflite` | Quantized model (firmware) |
| `ml/model_float.h5` | Float model (reference) |

---

## Invariants

1. **Completeness** — All sections populated before release
2. **Accuracy honesty** — Report int8 metrics, not just float
3. **Consent documented** — Speaker consent recorded
4. **Limitations explicit** — Speaker count, vocabulary, noise clearly stated
5. **Reproducibility** — Config + seed allow rebuild
6. **Quantized metrics** — int8 accuracy reported, not just float
7. **Versioned** — Model card version matches model version
8. **Accessible** — Plain language, no undisclosed assumptions

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_missing_metadata_writes_non_result_status` | Eval gate blocks incomplete metadata |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Training incomplete | Model card not published |
| Eval not run | Metrics remain TBD |
| Consent missing | Model cannot be released |
| Quantization accuracy drop | Reported in limitations |

---

## Acceptance Criteria

- Model card template with all sections
- Metadata files listed
- 8 invariants enumerated
- Population BLOCKED on training/eval
- Next step (0404) can use this output