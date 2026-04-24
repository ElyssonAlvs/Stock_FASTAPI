# imagem base
FROM python:3.14-slim

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

# copiar e tornar entrypoint executável
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# expor porta
EXPOSE 8000

# rodar app com migrations
ENTRYPOINT ["/app/entrypoint.sh"]