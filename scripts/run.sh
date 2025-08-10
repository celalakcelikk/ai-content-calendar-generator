#!/bin/bash
set -e
set -o pipefail

echo "📦 Loading environment variables..."
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "⚠️ No .env file found, proceeding with system defaults."
fi

echo "🚀 Starting AI Content Calendar Planner..."
streamlit run app.py
