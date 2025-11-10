# Agent Instructions for Metals Portfolio Tracker

## Project Overview

This is a **FastAPI web application** for tracking precious metals (Gold and Silver) portfolio performance with real-time pricing. Built with Python 3.14+, SQLAlchemy, and Jinja2 templates.

**Repository:** Monorepo - This project lives in `metals/` subdirectory.

**Tech Stack:** Python 3.14+, FastAPI, SQLAlchemy, Alembic, SQLite, uv package manager, Jinja2, Ruff (linting/formatting), mypy (type checking), pytest

## Critical Build & Validation Steps

### Installation & Setup (REQUIRED)

1. **ALWAYS install dependencies first** using `uv sync` (takes ~2 seconds)
   ```bash
   uv sync
   ```

2. **Environment setup:** A `.env` file with `DATABASE_URL` and `APP_ENV` must exist. Template at `.env.template`:
   ```bash
   cp .env.template .env
   ```

3. **Database migrations:** Run `uv run alembic upgrade head` after dependency installation to ensure schema is current.

### Validation Pipeline (Run in this exact order)

The GitHub Actions CI workflow (`.github/workflows/metals.yml`) runs these checks. **Run all of these locally before considering changes complete:**

```bash
# 1. Install with dev dependencies (REQUIRED for all checks)
uv sync --all-groups --locked

# 2. Type checking
uv run mypy .

# 3. Run tests
uv run pytest

# 4. Lint
uv run ruff check

# 5. Format check
uv run ruff format --check
```

**CRITICAL:** All 5 steps must pass. The workflow fails if any step fails. Order matters - type check and test before linting.

### Running the Application

```bash
uv run fastapi dev src/metals/main.py
```
Application runs at http://localhost:8000

### Docker Build

```bash
docker build -t metals:latest .
```
Uses Python 3.14 Alpine base with uv package manager (version specified in Dockerfile).

## Project Architecture

### Directory Structure

```
metals/
├── src/metals/              # Main application code
│   ├── main.py             # FastAPI app entry point with lifespan manager
│   ├── env.py              # Environment utilities
│   ├── internal/           # Core business logic
│   │   ├── persistency/    # Database layer
│   │   │   ├── models.py   # SQLAlchemy models (Portfolio, Holding, MetalPrice)
│   │   │   ├── db.py       # Session management
│   │   │   └── queries.py  # Database queries
│   │   ├── prices.py       # External price fetching
│   │   ├── price_cache.py  # Background price refresh service
│   │   ├── portfolio_calculations.py  # Portfolio value calculations
│   │   └── types.py        # Shared types (Metal enum)
│   ├── routers/            # FastAPI routers
│   │   ├── home.py         # Homepage
│   │   ├── portfolios.py   # Portfolio CRUD
│   │   ├── holdings.py     # Holdings CRUD
│   │   ├── shared.py       # Shared dependencies (Jinja2 templates)
│   │   └── types.py        # Router types
│   ├── templates/          # Jinja2 templates
│   └── static/             # CSS/JS assets
├── tests/
│   ├── conftest.py         # Pytest fixtures (test_session, client)
│   └── integration/        # Integration tests using TestClient
├── migrations/             # Alembic migrations
│   ├── env.py              # Alembic environment
│   └── versions/           # Migration files
├── db/                     # SQLite database (gitignored except .keep)
├── pyproject.toml          # Project config & dependencies
├── alembic.ini             # Alembic configuration
├── Dockerfile              # Production container
└── README.md               # Basic setup instructions
```

### Key Configuration Files

- **pyproject.toml**: Dependencies, mypy config (strict mode, `mypy_path = "src"`), pytest config (`pythonpath = ["src"]`), ruff config (E, F, I rules, excludes `migrations/`)
- **alembic.ini**: Migration config with `prepend_sys_path = src` (enables imports during migrations)
- **.env**: Required environment variables (DATABASE_URL, APP_ENV)
- **Dockerfile**: Multi-stage Alpine build using uv, runs on port 8080

### Database Models

Three main models in `src/metals/internal/persistency/models.py`:
- **Portfolio**: Container for holdings, cascade deletes
- **Holding**: Individual metal purchases (description, metal type, quantity, purchase_price)
- **MetalPrice**: Historical price data with composite index on (metal, created_at)

All models use UUID primary keys and timestamp tracking (created_at, updated_at).

## CI/CD Pipeline

GitHub Actions workflow at `.github/workflows/metals.yml` triggers on:
- All branch pushes affecting `metals/**` or workflow file
- Runs check job: type check → test → lint → format check
- Runs build job (master only): Docker build → save tarball → deploy via SCP

**The workflow uses `working-directory: ./metals` for all commands** - remember this is a monorepo.

## Common Pitfalls & Important Notes

1. **Monorepo context:** This project is in `metals/` subdirectory of a monorepo. GitHub Actions uses `working-directory: ./metals` for all commands.

2. **Python version:** Requires Python 3.14+. Check `pyproject.toml` for current `requires-python` version. CI enforces this.

3. **Import paths:** All imports use `from metals.*` because `pyproject.toml` sets `pythonpath = ["src"]` and alembic.ini sets `prepend_sys_path = src`.

4. **Database directory:** The `db/` directory must exist (tracked via `db/.keep`) but contents are gitignored.

5. **Ruff excludes migrations:** Don't run ruff checks on `migrations/` directory - it's excluded in config.

6. **Tests use in-memory SQLite:** Test fixtures in `conftest.py` create clean database per test using StaticPool and `:memory:`.

7. **Static files path:** Templates reference `/static/` which is mounted at `src/metals/static` in `main.py`.

8. **Background tasks:** App uses lifespan context manager to start/stop price refresh background task.

9. **Type checking scope:** CI uses `mypy .` which checks all Python files including tests. Both `mypy .` and `mypy src/` work.

## Working with This Codebase

**When making changes:**
1. Run `uv sync` first if pyproject.toml changed
2. Make surgical changes to relevant files
3. Run full validation pipeline (5 commands above)
4. Use pytest verbose mode (`pytest -v`) to see individual test results
5. Integration tests in `tests/integration/` cover main application routes

**When adding dependencies:**
- Add to `dependencies` in pyproject.toml, then run `uv sync`
- Dev dependencies go in `[dependency-groups].dev`

**When modifying database schema:**
- Create migration: `uv run alembic revision --autogenerate -m "description"`
- Apply: `uv run alembic upgrade head`
- Rollback: `uv run alembic downgrade -1`

**Trust these instructions.** Only search for additional information if something here is incomplete or incorrect.
