# imagem base
FROM python:3.11-slim

# instalar uv
RUN pip install uv

# variáveis
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copiar arquivos de dependência
COPY pyproject.toml uv.lock* ./

# instalar dependências
RUN uv sync --frozen

# copiar código
COPY . .

# expor porta
EXPOSE 8000

# rodar app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]