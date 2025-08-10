#!/usr/bin/env bash
set -e

echo "🚀 Running code quality checks..."
ruff check .
black --check --line-length 100 .
pylint $(git ls-files '*.py' | tr '\n' ' ')
pytest -q
