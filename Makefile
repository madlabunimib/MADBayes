.PHONY: test clean

test:
	pytest --cov-report=html --cov=madbayes --cov-append tests_python
	NUMBA_DISABLE_JIT=0 pytest --cov-report=html --cov=madbayes --cov-append tests_numba
	# NUMBA_DISABLE_JIT=1 pytest --cov-report=html --cov=madbayes --cov-append tests_numba

clean:
	find . -type d -name __pycache__ -exec rm -r {} \+
