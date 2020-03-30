.PHONY: test

test:
	pytest --cov-report=html --cov=weighted_imputation --cov-append tests_python
	NUMBA_DISABLE_JIT=0 pytest --cov-report=html --cov=weighted_imputation --cov-append tests_numba
	# NUMBA_DISABLE_JIT=1 pytest --cov-report=html --cov=weighted_imputation --cov-append tests_numba
