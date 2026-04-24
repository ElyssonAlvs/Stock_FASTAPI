#!/bin/bash
set -e

# Executar migrations
echo "Executando migrations..."
uv run alembic upgrade head

# Iniciar o servidor
echo "Iniciando servidor..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
