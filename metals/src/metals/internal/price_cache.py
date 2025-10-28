import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from metals.internal.prices import get_all_metal_prices_in_eur
from metals.internal.types import Metal

logger = logging.getLogger(__name__)


class PriceFetchError(Exception):
    """Raised when unable to fetch prices from external APIs."""

    pass


class PriceCache:
    """Async-safe cache for metal prices with background refresh."""

    def __init__(self, refresh_interval_seconds: int = 300):
        """
        Initialize price cache.

        Args:
            refresh_interval_seconds: How often to refresh prices
                (default: 300 = 5 minutes)
        """
        self._prices: Optional[dict[Metal, float]] = None
        self._last_updated: Optional[datetime] = None
        self._lock = asyncio.Lock()
        self._refresh_interval = timedelta(seconds=refresh_interval_seconds)
        self._background_task: Optional[asyncio.Task[None]] = None

    async def get_prices(self) -> dict[Metal, float]:
        """
        Get current metal prices from cache.

        If cache is empty, fetches prices immediately.

        Returns:
            Dictionary mapping Metal to price in EUR

        Raises:
            PriceFetchError: If cache is empty and fetching prices fails
        """
        async with self._lock:
            if self._prices is None:
                logger.info("Cache miss - fetching prices immediately")
                await self._fetch_prices()

                # If fetch failed and prices are still None, raise an error
                if self._prices is None:
                    raise PriceFetchError("Unable to fetch prices from external APIs")

            return self._prices.copy()

    async def _fetch_prices(self) -> None:
        """Fetch prices from external APIs and update cache."""
        try:
            self._prices = await get_all_metal_prices_in_eur()
            self._last_updated = datetime.now()
            logger.info(f"Prices updated successfully at {self._last_updated}")
        except Exception as e:
            logger.error(f"Failed to fetch prices: {e}")
            # Keep old prices if fetch fails

    async def _refresh_loop(self) -> None:
        """Background task that periodically refreshes prices."""
        logger.info(f"Starting price refresh loop (interval: {self._refresh_interval})")

        # Initial fetch
        async with self._lock:
            await self._fetch_prices()

        # Periodic refresh
        while True:
            await asyncio.sleep(self._refresh_interval.total_seconds())
            async with self._lock:
                await self._fetch_prices()

    def start_background_refresh(self) -> None:
        """Start the background refresh task."""
        if self._background_task is None:
            try:
                self._background_task = asyncio.create_task(self._refresh_loop())
                logger.info("Background price refresh task started")
            except Exception as e:
                logger.error(f"Failed to start background refresh task: {e}")
                raise

    async def stop_background_refresh(self) -> None:
        """Stop the background refresh task."""
        if self._background_task is not None:
            self._background_task.cancel()

            try:
                await self._background_task
            except asyncio.CancelledError:
                pass

            self._background_task = None

            logger.info("Background price refresh task stopped")


# Global cache instance
_price_cache: Optional[PriceCache] = None


def get_price_cache() -> PriceCache:
    """
    Get the global price cache instance.

    Note: This function is first called during application startup (in the lifespan
    context), which initializes the singleton before any request handlers run. This
    ensures the singleton pattern is safe in FastAPI's single-threaded event loop.
    """
    global _price_cache

    if _price_cache is None:
        _price_cache = PriceCache()

    return _price_cache
