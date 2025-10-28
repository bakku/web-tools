import os
from typing import Any

from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from metals.internal.persistency.db import engine
from metals.internal.persistency.queries import get_latest_metal_prices

templates = Jinja2Templates(directory="src/metals/templates")


def _is_development_mode() -> bool:
    return os.getenv("APP_ENV", "").lower() == "development"


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
        with Session(engine) as session:
            metal_prices = get_latest_metal_prices(session)
        context["metal_prices"] = metal_prices if metal_prices else None
    except Exception:
        # Prices not available, template will handle missing prices gracefully
        context["metal_prices"] = None

    context["is_dev_mode"] = _is_development_mode()

    return context
