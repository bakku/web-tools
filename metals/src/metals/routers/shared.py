from typing import Any

from fastapi.templating import Jinja2Templates

from ..internal.price_cache import PriceFetchError, get_price_cache

templates = Jinja2Templates(directory="src/metals/templates")


async def get_template_context(**kwargs: Any) -> dict[str, Any]:
    """
    Get template context with metal prices injected.

    Args:
        **kwargs: Additional context variables to include

    Returns:
        Dictionary with all context variables including metal_prices
    """
    context = dict(kwargs)

    # Try to get metal prices, but don't fail if unavailable
    try:
        cache = get_price_cache()
        metal_prices = await cache.get_prices()
        context["metal_prices"] = metal_prices
    except PriceFetchError:
        # Prices not available, template will handle missing prices gracefully
        context["metal_prices"] = None

    return context
