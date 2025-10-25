import os
from typing import Any

from fastapi.templating import Jinja2Templates

from ..internal.price_cache import PriceFetchError, get_price_cache

templates = Jinja2Templates(directory="src/metals/templates")


def is_development_mode() -> bool:
    """
    Check if the application is running in development mode.

    Returns:
        True if running in development mode, False otherwise.
    """
    # Check for common development environment indicators
    return os.getenv("ENVIRONMENT", "").lower() in ("dev", "development") or os.getenv(
        "DEBUG", ""
    ).lower() in ("1", "true", "yes")


async def build_template_context(**kwargs: Any) -> dict[str, Any]:
    """
    Builds template context with shared values such as metal prices automatically
    included.

    Args:
        **kwargs: Additional context variables to include

    Returns:
        Dictionary with all context variables including shared values.
    """
    context = dict(kwargs)

    try:
        cache = get_price_cache()
        metal_prices = await cache.get_prices()
        context["metal_prices"] = metal_prices
    except PriceFetchError:
        # Prices not available, template will handle missing prices gracefully
        context["metal_prices"] = None

    # Add development mode flag
    context["is_dev_mode"] = is_development_mode()

    return context
