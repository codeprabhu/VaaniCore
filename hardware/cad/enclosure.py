"""Parametric VaaniCore enclosure generator.

This file intentionally does not contain fabricated render outputs.  When CadQuery
is installed it creates the two simple enclosure halves and exports STEP/STL files;
the team must inspect fit, acoustics, and printability before treating them as a
design result.
"""
from __future__ import annotations

import argparse
import pathlib
import sys


def build(args: argparse.Namespace) -> int:
    try:
        import cadquery as cq
    except ImportError:
        print("BLOCKED_TOOLCHAIN: install CadQuery to generate native enclosure files", file=sys.stderr)
        return 2

    out = pathlib.Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    length, width, height = args.length, args.width, args.height
    wall = args.wall
    lower_h = height / 2

    # Coordinate origin is the enclosure centre in XY and the bottom face in Z.
    lower = (
        cq.Workplane("XY")
        .box(length, width, lower_h, centered=(True, True, False))
        .faces(">Z")
        .shell(-wall)
    )
    upper = (
        cq.Workplane("XY")
        .workplane(offset=lower_h)
        .box(length, width, lower_h, centered=(True, True, False))
        .faces(">Z")
        .shell(-wall)
    )

    # Conservative through-cuts are reference features, not a claim of board fit.
    upper = upper.faces(">Z").workplane().rect(args.oled_window_x, args.oled_window_y).cutBlind(-wall * 2)
    upper = upper.faces(">X").workplane().rect(args.usb_cutout_y, args.usb_cutout_z).cutBlind(-wall * 2)
    lower = lower.faces(">Y").workplane().hole(args.mic_port, depth=wall * 2)

    cq.exporters.export(lower, str(out / "vaanicore_lower.step"))
    cq.exporters.export(upper, str(out / "vaanicore_upper.step"))
    cq.exporters.export(lower, str(out / "vaanicore_lower.stl"))
    cq.exporters.export(upper, str(out / "vaanicore_upper.stl"))
    print(f"generated CadQuery STEP/STL files under {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the VaaniCore parametric enclosure with CadQuery")
    parser.add_argument("--output", default="hardware/cad/out")
    parser.add_argument("--length", type=float, default=70.0, help="overall length in mm")
    parser.add_argument("--width", type=float, default=50.0, help="overall width in mm")
    parser.add_argument("--height", type=float, default=22.0, help="overall height in mm")
    parser.add_argument("--wall", type=float, default=2.0, help="wall thickness in mm")
    parser.add_argument("--oled-window-x", type=float, default=32.0)
    parser.add_argument("--oled-window-y", type=float, default=18.0)
    parser.add_argument("--usb-cutout-y", type=float, default=10.0)
    parser.add_argument("--usb-cutout-z", type=float, default=5.0)
    parser.add_argument("--mic-port", type=float, default=1.5, help="mic port diameter in mm")
    args = parser.parse_args()
    if min(args.length, args.width, args.height, args.wall) <= 0 or args.wall >= args.height / 2:
        parser.error("dimensions must be positive and wall must be less than half the height")
    return build(args)


if __name__ == "__main__":
    raise SystemExit(main())
