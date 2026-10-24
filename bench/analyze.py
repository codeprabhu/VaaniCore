"""Analyze labelled virtual trials and generate 300-dpi figures."""
from __future__ import annotations
import argparse, csv, json, pathlib, os

def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze benchmark CSV and generate labelled figures")
    parser.add_argument("--input", default="results/virtual_trials.csv")
    parser.add_argument("--figures", action="store_true")
    args = parser.parse_args()
    rows = list(csv.DictReader(pathlib.Path(args.input).open()))
    summary = {"input": args.input, "rows": len(rows), "label": "SIMULATED", "note": "Virtual device only; not hardware evidence."}
    print(json.dumps(summary, indent=2))
    if not args.figures:
        return
    mpl_config = pathlib.Path("/tmp/vaanicore-matplotlib"); mpl_config.mkdir(parents=True, exist_ok=True); os.environ.setdefault("MPLCONFIGDIR", str(mpl_config))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    out = pathlib.Path("results/figures"); out.mkdir(parents=True, exist_ok=True)
    latency = [float(row["latency_ms"]) for row in rows]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot([latency], tick_labels=["P1 virtual"])
    ax.set_ylabel("Dispatch latency (ms)"); ax.set_title("SIMULATED — virtual protocol path")
    fig.tight_layout(); fig.savefig(out / "virtual_latency_boxplot.png", dpi=300); plt.close(fig)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["P1 target", "P2 target"], [80, 64000], color=["#4C78A8", "#F2CF5B"])
    ax.set_yscale("log"); ax.set_ylabel("USB bytes / command"); ax.set_title("TARGET — traffic budget, not measured")
    fig.tight_layout(); fig.savefig(out / "traffic_target.png", dpi=300); plt.close(fig)
    (out / "README.txt").write_text("Figures are generated from virtual trials or TARGET budgets and must not be presented as hardware measurements.\n")

if __name__ == "__main__":
    main()
