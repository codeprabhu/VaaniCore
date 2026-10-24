from __future__ import annotations
import argparse
def main():
    p=argparse.ArgumentParser(); p.add_argument('--help-only', action='store_true'); p.parse_args(); print('training blocked until labelled dataset exists')
if __name__ == '__main__': main()
