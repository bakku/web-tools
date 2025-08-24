FROM ghcr.io/astral-sh/uv:0.8.13-python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock .

RUN uv sync --locked --no-dev

COPY . .

CMD [".venv/bin/fastapi", "run", "src/masstimes/main.py", "--port", "8080"]