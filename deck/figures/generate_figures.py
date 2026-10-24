"""Generate the architecture hero figure from the VaaniCore block specification."""
from __future__ import annotations
import argparse, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOT = '''digraph VaaniCore {
  graph [rankdir=LR, bgcolor="transparent", pad="0.2"];
  node [shape=box, style="rounded,filled", fontname="Arial", color="#263238", fillcolor="#E8F1F5"];
  mic [label="INMP441\\nI2S mic"];
  dma [label="GDMA\\ndouble buffer"];
  dsp [label="VAD + MFCC10\\nint8 classifier"];
  ctx [label="Intent +\\nNVS context"];
  usb [label="USB-CDC\\nCRC16"];
  host [label="Allow-listed\\nhost agent"];
  sim [label="ngspice\\nproject result"];
  mic -> dma -> dsp -> ctx -> usb -> host -> sim;
  p1 [label="P1 full-edge", shape=note, fillcolor="#D9F2D9"];
  p2 [label="P2 hybrid", shape=note, fillcolor="#FFF0C2"];
  p3 [label="P3 host-only", shape=note, fillcolor="#F8D7DA"];
  {rank=same; p1; p2; p3;}
}
'''

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate architecture SVG")
    parser.add_argument("--output", default="deck/assets/architecture.svg")
    args = parser.parse_args()
    output = ROOT / args.output; output.parent.mkdir(parents=True, exist_ok=True)
    dot_path = output.with_suffix(".dot"); dot_path.write_text(DOT)
    try:
        subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(output)], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Graphviz figure generation failed: {exc}")
    print(output)
    return 0
if __name__ == "__main__": raise SystemExit(main())
