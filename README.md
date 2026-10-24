# VaaniCore

Bootstrap implementation for the Stage-2 embedded edge-AI coprocessor. The verified offline vertical slice is:

`typed intent → CRC16 frame → allow-list/path-jail host dispatcher → typed status`

Repository root: `/home/shrivathssp/Desktop/VaaniCore`.

Run:

- `make test` — standard-library security and protocol tests.
- `make sim-demo` — virtual device loop; outputs are `SIMULATED`, not hardware measurements.
- `make bench` — writes a labelled simulated benchmark summary.
- `make deck-draft` — checks data/placeholder state; the official PPTX is still required for a real deck.

See `TODO_HUMAN.md` for the first human actions. No hardware, audio dataset, official template, citations, prices, photos, mentor sign-off, or measured result is fabricated here.
