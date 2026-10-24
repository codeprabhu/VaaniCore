.PHONY: test sim-demo bench deck-draft deck-final
PYTHON ?= python3

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

sim-demo:
	PYTHONPATH=. $(PYTHON) -m host.tools.virtual_device --project amplifier

bench:
	PYTHONPATH=. $(PYTHON) bench/run_benchmarks.py

smoke:
	PYTHONPATH=. $(PYTHON) ml/smoke_test.py

dsp-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/dsp tests/dsp_parity.c firmware/components/dsp/mfcc.c -lm -o /tmp/vaanicore_dsp_test
	/tmp/vaanicore_dsp_test

protocol-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/protocol tests/protocol_c.c firmware/components/protocol/protocol.c firmware/components/protocol/crc16.c -o /tmp/vaanicore_protocol_test
	/tmp/vaanicore_protocol_test

deck-draft:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --draft

deck-final:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --final
