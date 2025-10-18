import httpx

from .models import Metal


async def _get_metal_price_in_usd(metal: Metal) -> float:
    async with httpx.AsyncClient() as client:
        symbol = "XAU" if metal == "Gold" else "XAG"
        response = await client.get(
            f"https://gold-api.com/price/{symbol}",
            timeout=10.0,
        )
        response.raise_for_status()
        data = response.json()
        return float(data["price_usd"])


async def _get_usd_to_eur_rate() -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.frankfurter.app/latest?from=USD&to=EUR",
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
