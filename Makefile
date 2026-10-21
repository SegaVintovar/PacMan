
install:
	@echo "installing packages and dependencies"
	@uv sync

run:
	@echo "running Pac Man"
	@uv run python -m src config.json

clean:
	@echo "cleansing __pycache__"
	@rm -rf ./__pycache__
	@rm -rf ./src/__pycache__
	@rm -rf ./.mypy_cache
	@rm -rf .venv

lint:
	echo "linty linty"

lint-strict:
	echo "linty linty on the juice"