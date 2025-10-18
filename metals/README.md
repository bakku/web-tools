# Metals Portfolio Tracker

A web application for tracking precious metals (Gold and Silver) portfolio performance with real-time pricing.

## Setup

### Prerequisites

- Python 3.14 or higher
- uv package manager

### Installation

Install dependencies:
```bash
uv sync
```

### Running the Application

```bash
uv run fastapi dev src/metals/main.py
```

The application will be available at http://localhost:8000

## Development

### Linting

```bash
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```
