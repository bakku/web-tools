# Metals Portfolio Tracker

A web application for tracking precious metals (Gold and Silver) portfolio performance with real-time pricing.

## Features

- Create and manage multiple portfolios
- Track holdings of Gold and Silver
- Real-time pricing from gold-api.com
- Automatic USD to EUR conversion
- Calculate gains/losses and portfolio performance

## Setup

### Prerequisites

- Python 3.14 or higher
- uv package manager

### Installation

1. Install dependencies:
```bash
uv sync
```

2. Obtain a Gold API key:
   - Visit [gold-api.com](https://www.gold-api.com/) and sign up for a free account
   - Copy your API key

3. Set the API key as an environment variable:
```bash
export GOLD_API_KEY="your-api-key-here"
```

### Running the Application

```bash
uv run fastapi dev src/metals/main.py
```

The application will be available at http://localhost:8000

### How It Works

When you view a portfolio, the application:
1. Fetches current gold and silver prices in USD from gold-api.com
2. Fetches the USD to EUR exchange rate from frankfurter.dev
3. Calculates metal prices in EUR
4. Computes your portfolio value, gains, and losses based on real-time prices

**Note**: If the APIs are unavailable or the API key is invalid, you'll see a 503 Service Unavailable error when viewing portfolios.

## API Dependencies

This application uses the following external APIs:

- **gold-api.com**: Provides real-time gold and silver prices in USD
  - Requires API key (free tier available)
  - Documentation: https://www.gold-api.com/api-docs

- **frankfurter.dev**: Provides currency exchange rates (USD to EUR)
  - Free, no authentication required
  - Documentation: https://www.frankfurter.app/docs/

## Development

### Linting

```bash
uv run ruff check src/
```

### Type Checking

```bash
uv run mypy src/
```
