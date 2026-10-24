.PHONY: test sim-demo bench deck-draft deck-final
PYTHON ?= python3

test: protocol-test context-test dsp-test
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

sim-demo:
	PYTHONPATH=. $(PYTHON) -m host.tools.virtual_device --project amplifier
	PYTHONPATH=. $(PYTHON) host/tools/stdio_demo.py

bench:
	PYTHONPATH=. $(PYTHON) bench/run_benchmarks.py
	PYTHONPATH=. $(PYTHON) bench/analyze.py --figures
	PYTHONPATH=. $(PYTHON) bench/analyze_timing.py

smoke:
	PYTHONPATH=. $(PYTHON) ml/smoke_test.py

audit:
	PYTHONPATH=. $(PYTHON) tools/audit_phase_a.py

dsp-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/dsp tests/dsp_parity.c firmware/components/dsp/mfcc.c -lm -o /tmp/vaanicore_dsp_test
	/tmp/vaanicore_dsp_test

protocol-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/protocol tests/protocol_c.c firmware/components/protocol/protocol.c firmware/components/protocol/crc16.c -o /tmp/vaanicore_protocol_test
	/tmp/vaanicore_protocol_test

context-test:
	$(CC) -std=c11 -O2 -Ifirmware/components/context tests/context_c.c firmware/components/context/context.c -o /tmp/vaanicore_context_test
	/tmp/vaanicore_context_test

deck-draft:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --draft

figures:
	$(PYTHON) deck/figures/generate_figures.py

deck-final:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --final
