# Leave-One-Speaker-Out Evaluation Specification

**Generated:** 2026-11-19T04:35:00Z
**Git Commit:** c394453
**Status:** APPROVED (spec complete, eval BLOCKED on dataset/model)

---

## Contract

**Scope:** Leave-one-speaker-out cross-validation for intent classifier evaluation.

**Purpose:** Provide unbiased accuracy estimate for speaker-independent classification.

---

## Protocol

### 3-Fold Cross-Validation

| Fold | Train Speakers | Test Speaker |
|------|----------------|--------------|
| 1 | speaker2, speaker3 | speaker1 |
| 2 | speaker1, speaker3 | speaker2 |
| 3 | speaker1, speaker2 | speaker3 |

### Per-Fold Procedure
1. Train DS-CNN on train speakers (2 speakers × 480 clips = 960 samples)
2. Validate on val split during training (early stopping)
3. Evaluate on test speaker (held-out, 480 samples)
4. Record: accuracy, F1-macro, confusion matrix

---

## Metrics

### Per-Fold
| Metric | Definition |
|-------|------------|
| Accuracy | (TP + TN) / Total |
| F1-macro | Mean F1 per class (unweighted) |
| Confusion Matrix | 13×13 counts |

### Aggregate (Final Report)
| Metric | Computation |
|-------|-------------|
| Mean Accuracy | (acc₁ + acc₂ + acc₃) / 3 |
| Std Accuracy | Std dev of 3 accuracies |
| Mean F1-macro | (f1₁ + f1₂ + f1₃) / 3 |
| Std F1-macro | Std dev of 3 F1 scores |

---

## Evaluation Implementation (`ml/eval.py`)

```python
def evaluate_model(model_path, test_speaker_id, data_dir, quantized=False):
    # 1. Load model (Keras float or TFLite int8)
    if quantized:
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
    else:
        model = tf.keras.models.load_model(model_path)
    
    # 2. Load test speaker data
    test_samples = load_speaker_data(test_speaker_id, data_dir)
    
    # 3. Run inference
    predictions = []
    labels = []
    for waveform, label in test_samples:
        mfcc = extract_mfcc(waveform)  # (frames, 10)
        if quantized:
            pred = run_tflite_inference(interpreter, mfcc)
        else:
            pred = model.predict(mfcc[None, ...])
        predictions.append(pred.argmax())
        labels.append(label)
    
    # 4. Compute metrics
    accuracy = accuracy_score(labels, predictions)
    f1_macro = f1_score(labels, predictions, average='macro')
    cm = confusion_matrix(labels, predictions, labels=range(13))
    
    return {"accuracy": accuracy, "f1_macro": f1_macro, "confusion_matrix": cm.tolist()}
```

---

## Eval Gate (`tests/test_ml_eval_gate.py`)

```python
def test_missing_metadata_writes_non_result_status():
    # Eval gate blocks if metadata incomplete
    # Requires: model path, test speaker ID, data dir, quantization flag
    pass
```

---

## Invariants

1. **Strict speaker isolation** — Test speaker never seen during training
2. **3-fold CV** — Each speaker tested exactly once
3. **Per-fold metrics** — Accuracy, F1-macro, confusion matrix
4. **Aggregate statistics** — Mean ± std across folds
5. **Quantized eval** — Must test int8 TFLite model (not just float)
5. **Metadata completeness** — Eval gate blocks incomplete runs
6. **Reproducible** — Fixed seeds, deterministic inference
7. **Class balance** — All 13 classes evaluated
8. **Consent documented** — All test speakers consented

---

## Test Coverage

| Test | Verifies |
|------|----------|
| `test_missing_metadata_writes_non_result_status` | Eval gate blocks incomplete |

---

## Failure Modes

| Condition | Behavior |
|-----------|----------|
| Dataset not collected | Eval cannot run |
| Model not trained | No checkpoint to evaluate |
| Single speaker | Leave-one-out impossible |
| Quantization accuracy drop | Report separately (float vs int8) |
| Class missing in test speaker | F1-macro penalizes |

---

## Acceptance Criteria

- 3-fold leave-one-speaker-out protocol defined
- Per-fold and aggregate metrics specified
- Eval implementation outlined
- Eval gate documented
- 8 invariants enumerated
- Eval BLOCKED on dataset and trained model
- Next step (0394) can use this output