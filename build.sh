#!/usr/bin/env bash
# Build script para Render (si no usas Docker)
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
