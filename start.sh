#!/usr/bin/env bash
# Start script para Render (si no usas Docker)
uvicorn main:app --host 0.0.0.0 --port $PORT
