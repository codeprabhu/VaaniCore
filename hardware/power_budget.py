from __future__ import annotations
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument('--mcu-w', type=float, default=0.4); p.add_argument('--peripherals-w', type=float, default=0.2); a=p.parse_args()
    print(f"TARGET total_power_w={a.mcu_w+a.peripherals_w:.3f} label=TARGET")
if __name__ == '__main__': main()
