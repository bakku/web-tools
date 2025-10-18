FROM ghcr.io/astral-sh/uv:0.9.4-python3.14-alpine

WORKDIR /app

RUN apk add --no-cache \
    build-base
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY . .

CMD [".venv/bin/fastapi", "run", "src/metals/main.py", "--port", "8080"]
