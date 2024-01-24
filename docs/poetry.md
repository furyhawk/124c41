# poetry

```zsh
# Install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install dependencies
poetry install

# Run
poetry run python main.py

# Run tests
poetry run pytest

# Run tests with coverage and open in browser
poetry run pytest --cov=src --cov-report=html && open htmlcov/index.html

# Fix poetry shell not activating virtualenv
source "$( poetry env list --full-path | grep Activated | cut -d' ' -f1 )/bin/activate"


```