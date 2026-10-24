from __future__ import annotations
import argparse, json, pathlib
def main():
    p=argparse.ArgumentParser(description='Summarize labelled benchmark output'); p.add_argument('--input', default='results/summary.json'); a=p.parse_args(); d=json.loads(pathlib.Path(a.input).read_text()); print(json.dumps({'provenance': d.get('provenance'), 'metric_count': len(d.get('metrics', {}))}, indent=2))
if __name__ == '__main__': main()
