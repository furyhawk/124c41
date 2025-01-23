# poetry

```zsh
# Install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Update Poetry
poetry self update

# Run
poetry run python main.py

# Run tests
poetry run pytest

# Run tests with coverage and open in browser
poetry run pytest --cov=src --cov-report=html && open htmlcov/index.html

# Fix poetry shell not activating virtualenv
source "$( poetry env list --full-path | grep Activated | cut -d' ' -f1 )/bin/activate"

# Add from requirements.txt
poetry add $(cat requirements.txt)
# or
cat requirements.txt | xargs poetry add

```