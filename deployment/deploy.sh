#!/bin/bash
# Enterprise ADK Production Deployment Pipeline Trigger
set -e

echo "===================================================="
echo "Starting Enterprise ADK Deployment Flow"
echo "===================================================="

# 1. Lint and Static Analysis
echo "Step 1: Running code quality lints..."
agents-cli lint

# 2. Run pytest suite
echo "Step 2: Running automated unit and integration tests..."
uv run pytest

# 3. Quality evaluation check
echo "Step 3: Running agent quality evaluation..."
uv run python eval/evaluation_runner.py

# 4. Agent deployment
echo "Step 4: Deploying agent to Google Cloud Platform..."
# Read deployment target from manifest or override via flag
agents-cli deploy --yes

echo "===================================================="
echo "Deployment Pipeline Complete!"
echo "===================================================="
