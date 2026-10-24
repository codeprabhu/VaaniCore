from __future__ import annotations
import argparse
def main():
    p=argparse.ArgumentParser(description='Export the trained int8 model after dataset and training are available'); p.add_argument('--output', default='firmware/components/model/model_data.cc'); p.parse_args(); print('blocked: no trained model or TensorFlow toolchain is present')
if __name__ == '__main__': main()
