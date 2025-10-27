from typing import Literal

import httpx

from .types import Metal

Symbol = Literal["XAU", "XAG"]

GOLD_API_BASE_URL = "https://api.gold-api.com/"
FRANKFURTER_API_BASE_URL = "https://api.frankfurter.app/"

METAL_TO_SYMBOL: dict[Metal, Symbol] = {"Gold": "XAU", "Silver": "XAG"}


async def _get_metal_price_in_usd(metal: Metal) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GOLD_API_BASE_URL}price/{METAL_TO_SYMBOL[metal]}",
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        return float(data["price"])


async def _get_usd_to_eur_rate() -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{FRANKFURTER_API_BASE_URL}latest?from=USD&to=EUR",
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        return float(data["rates"]["EUR"])


async def get_all_metal_prices_in_eur() -> dict[Metal, float]:
    usd_to_eur = await _get_usd_to_eur_rate()

    metals: list[Metal] = ["Gold", "Silver"]
    prices: dict[Metal, float] = {}

    for metal in metals:
        usd_price = await _get_metal_price_in_usd(metal)
        prices[metal] = usd_price * usd_to_eur

    return prices
