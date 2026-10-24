from __future__ import annotations
import argparse, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from tools.provenance import generated_provenance
def main():
    p=argparse.ArgumentParser(); p.add_argument('--mcu-w', type=float, default=0.4); p.add_argument('--peripherals-w', type=float, default=0.2); p.add_argument('--output', default='results/power_budget.json'); a=p.parse_args()
    total = a.mcu_w + a.peripherals_w
    output = ROOT / a.output; output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'provenance': generated_provenance({'mcu_w': a.mcu_w, 'peripherals_w': a.peripherals_w}), 'label': 'TARGET', 'mcu_w': a.mcu_w, 'peripherals_w': a.peripherals_w, 'total_power_w': total}, indent=2) + '\n')
    print(f"TARGET total_power_w={total:.3f} label=TARGET; {output}")
if __name__ == '__main__': main()
