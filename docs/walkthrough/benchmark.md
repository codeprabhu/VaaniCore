# Benchmark walkthrough

`bench/run_benchmarks.py` creates 30 virtual protocol trials and records CSV provenance. `bench/analyze.py` computes a virtual latency box plot and target traffic plot. `bench/analyze_timing.py` rejects placeholder timing rows and only emits `MEASURED` after numeric manual/voice inputs exist.

Viva questions: Why N≥30? It gives a basic distribution rather than one lucky timing. Why p95? Tail latency matters to interaction. Why label virtual data? It is not board evidence. Why keep CSV? It preserves trial-level auditability. What remains? P1/P2/P3 hardware/host experiments and power measurements.
