"""Analytical enclosure checks; outputs are ESTIMATE, never measured FEA."""
from __future__ import annotations
import argparse, json, pathlib

def main() -> int:
    p = argparse.ArgumentParser(description="Estimate snap-fit strain and boss bending")
    p.add_argument('--thickness-mm', type=float, default=2.0)
    p.add_argument('--cantilever-mm', type=float, default=12.0)
    p.add_argument('--deflection-mm', type=float, default=1.0)
    p.add_argument('--output', default='results/enclosure_estimate.json')
    a = p.parse_args()
    strain = 3 * a.thickness_mm * a.deflection_mm / (2 * a.cantilever_mm * a.cantilever_mm)
    data = {'label': 'ESTIMATE', 'model': 'cantilever strain epsilon=3*t*y/(2*L^2)', 'inputs_mm': vars(a), 'snap_fit_strain': strain, 'allowable_strain': None, 'status': 'requires PETG datasheet verification'}
    out = pathlib.Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(data, indent=2) + '\n')
    print(out)
    return 0
if __name__ == '__main__': raise SystemExit(main())
