#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Training and verifying ML models..."
python backend/train_models.py

echo "==> Installing frontend dependencies and building React SPA..."
npm --prefix frontend install
npm --prefix frontend run build

echo "==> NetGuard AI build complete!"
