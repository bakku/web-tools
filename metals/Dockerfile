FROM ghcr.io/astral-sh/uv:0.8.13-python3.14-alpine

WORKDIR /app

COPY pyproject.toml uv.lock .

RUN uv sync --locked --no-dev

COPY . .

CMD [".venv/bin/fastapi", "run", "src/metals/main.py", "--port", "8080"]
