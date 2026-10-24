# ML pipeline walkthrough

`tools/record_dataset.py` is the human recording interface. It captures 16 kHz mono `int16` WAV files through the optional `sounddevice` backend, trims low-energy leading/trailing samples, flags clipping, and appends `metadata.csv` plus provenance. If the backend or microphone is unavailable it exits without writing audio. `ml/dataset.py` validates metadata and constructs leave-one-speaker-out partitions. `ml/features.py` supplies MFCCs. Training/TFLite export remain gated because no labelled recordings or TensorFlow/TFLite toolchain exist in the workspace.

Viva questions: Why leave one speaker out? To measure unseen-speaker generalisation. Why record distance and room? To stratify acoustic conditions. Why a closed vocabulary? It fits MCU memory and safety constraints. Why confidence gating? Low-confidence commands must never act. What is currently reported? Only metadata/synthetic pipeline checks, never accuracy.
