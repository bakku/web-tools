"""Service for fetching real-time metal prices and currency conversion."""

import httpx

from .models import Metal


async def get_metal_price_in_usd(metal: Metal) -> float:
    """
    Fetch the current price of a metal in USD per ounce from gold-api.com.
    
    Args:
        metal: The metal type (Gold or Silver)
        
    Returns:
        Price per troy ounce in USD
        
    Raises:
        httpx.HTTPError: If the API request fails
    """
    async with httpx.AsyncClient() as client:
        # gold-api.com uses 'gold' and 'silver' as metal names
        metal_name = metal.lower()
        
        response = await client.get(
            f"https://gold-api.com/price/{metal_name}",
            timeout=10.0,
        )
        response.raise_for_status()
        
        data = response.json()
        # The API returns price per troy ounce in USD
        return float(data["price_usd"])


async def get_usd_to_eur_rate() -> float:
    """
    Fetch the current USD to EUR exchange rate from frankfurter.dev.
    
    Returns:
        Exchange rate (1 USD = X EUR)
        
    Raises:
        httpx.HTTPError: If the API request fails
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.frankfurter.app/latest?from=USD&to=EUR",
            timeout=10.0,
        )
        response.raise_for_status()
        
        data = response.json()
        return float(data["rates"]["EUR"])


async def get_metal_price_in_eur(metal: Metal) -> float:
    """
    Fetch the current price of a metal in EUR per ounce.
    
    Combines gold-api.com (for USD price) and frankfurter.dev (for USD/EUR rate).
    
    Args:
        metal: The metal type (Gold or Silver)
        
    Returns:
        Price per troy ounce in EUR
        
    Raises:
        httpx.HTTPError: If any API request fails
    """
    # Fetch both prices concurrently
    usd_price = await get_metal_price_in_usd(metal)
    usd_to_eur = await get_usd_to_eur_rate()
    
    return usd_price * usd_to_eur


async def get_all_metal_prices_in_eur() -> dict[Metal, float]:
    """
    Fetch current prices for all supported metals in EUR per ounce.
    
    Returns:
        Dictionary mapping metal types to their current prices in EUR
        
    Raises:
        httpx.HTTPError: If any API request fails
    """
    # Fetch the exchange rate once
    usd_to_eur = await get_usd_to_eur_rate()
    
    # Fetch metal prices concurrently
    metals: list[Metal] = ["Gold", "Silver"]
    prices: dict[Metal, float] = {}
    
    for metal in metals:
        usd_price = await get_metal_price_in_usd(metal)
        prices[metal] = usd_price * usd_to_eur
    
    return prices
