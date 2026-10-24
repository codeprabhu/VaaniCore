# Dataset walkthrough

`ml/dataset.py` requires explicit clip path, label, speaker, distance, and room metadata. It creates leave-one-speaker-out partitions by speaker ID, never by random clip, and labels its output as a metadata check. Accuracy remains absent until the model and real recordings exist.

Viva questions: Why hold out speakers? To test generalisation. Why keep room/distance? To stratify conditions. Why no synthetic score? It would not represent the team’s voices. What does the validator produce? Counts and split sizes only. What must follow? Train/export/evaluate and save `results/ml_eval.json` with provenance.
