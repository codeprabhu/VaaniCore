from __future__ import annotations
import argparse, json, pathlib
from ml.dataset import read_metadata, summary
def main():
    p=argparse.ArgumentParser(description='Validate speaker metadata before evaluation'); p.add_argument('--metadata'); p.add_argument('--output', default='results/ml_metadata_check.json'); a=p.parse_args()
    if not a.metadata:
        print('evaluation blocked until labelled metadata exists; no score generated'); return
    data=summary(read_metadata(a.metadata)); out=pathlib.Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(data, indent=2) + '\n'); print(out)
if __name__ == '__main__': main()
