format:
	isort . --sp .isort.cfg --skip corpora --skip Dockerfile
	black . -l 99

lint:
	find . -iname "*.py" | xargs pylint --rcfile=.pylintrc || exit 0

lint-report:
	find . -iname "*.py" | xargs pytest --pylint --pylint-rcfile=.pylintrc --flake8 || exit 0

typehint:
	find . -iname "*.py" | xargs mypy --ignore-missing-imports --show-error-codes --pretty --strict || exit 0
	# find . -iname "*.py" | xargs pytest --pylint --pylint-rcfile=.pylintrc --flake8 --mypy --mypy-ignore-missing-imports
