install:
	@echo "installing packages and dependencies"
	@uv sync

run:
	@echo "running Pac Man"
	@uv run python pac-man.py config.json


clean:
	@echo "cleansing __pycache__"
	@rm -rf ./__pycache__
	@rm -rf ./src/__pycache__
	@rm -rf ./.mypy_cache
	@rm -rf .venv

debug:
	uv run python -m pdb pac-man.py config.json

build:
	pyinstaller pac-man.py --name pacman --onedir --noconfirm \
  --add-data "src/assets:src/assets" --add-data "config.json:." --paths .

lint:
	flake8 .
	mypy . --warn-return-any\
	 --warn-unused-ignores\
	 --ignore-missing-imports\
	 --disallow-untyped-defs\
	 --check-untyped-defs

lint-strict:
	flake8 .
	uv run mypy . --strict
