import asyncio
import typing

import httpx

from metals.internal.types import Metal

Symbol = typing.Literal["XAU", "XAG"]

GOLD_API_BASE_URL = "https://api.gold-api.com/"
FRANKFURTER_API_BASE_URL = "https://api.frankfurter.app/"

METAL_TO_SYMBOL: dict[Metal, Symbol] = {Metal.GOLD: "XAU", Metal.SILVER: "XAG"}


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

    # PyTypeChecker incorrectly thinks that list(Metal) returns a list of str
    # noinspection PyTypeChecker
    metals: list[Metal] = list(Metal)

    coroutines = [_get_metal_price_in_usd(metal) for metal in metals]

    results = await asyncio.gather(*coroutines)

    return {
        metal: price * usd_to_eur for price, metal in zip(results, metals, strict=True)
    }
