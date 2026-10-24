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

deck-draft:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --draft

deck-final:
	PYTHONPATH=. $(PYTHON) deck/build_deck.py --final
