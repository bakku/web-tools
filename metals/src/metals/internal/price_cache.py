import asyncio
import logging
from datetime import timedelta

from sqlalchemy.orm import Session

from metals.internal.persistency.db import engine
from metals.internal.persistency.queries import insert_metal_price
from metals.internal.prices import get_all_metal_prices_in_eur

logger = logging.getLogger(__name__)


class PriceRefresher:
    """
    Background task that periodically fetches prices and stores them in the
    database.
    """

    def __init__(self, refresh_interval_seconds: int = 300):
        """
        Initialize price refresher.

        Args:
            refresh_interval_seconds: How often to refresh prices
                (default: 300 = 5 minutes)
        """
        self._refresh_interval = timedelta(seconds=refresh_interval_seconds)
        self._background_task: asyncio.Task[None] | None = None

    async def _fetch_and_store_prices(self) -> None:
        """Fetch prices from external APIs and store them in the database."""
        try:
            prices = await get_all_metal_prices_in_eur()

            with Session(engine) as session:
                for metal, price in prices.items():
                    insert_metal_price(session, metal, price)

            logger.info("Prices updated successfully and stored in database")
        except Exception as e:
            logger.error(f"Failed to fetch and store prices: {e}")

    async def _refresh_loop(self) -> None:
        """Background task that periodically refreshes prices."""
        logger.info(f"Starting price refresh loop (interval: {self._refresh_interval})")

        # Initial fetch
        await self._fetch_and_store_prices()

        # Periodic refresh
        while True:
            await asyncio.sleep(self._refresh_interval.total_seconds())
            await self._fetch_and_store_prices()

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


# Global refresher instance
_price_refresher: PriceRefresher | None = None


def get_price_refresher() -> PriceRefresher:
    """
    Get the global price refresher instance.

    Note: This function is first called during application startup (in the lifespan
    context), which initializes the singleton before any request handlers run. This
    ensures the singleton pattern is safe in FastAPI's single-threaded event loop.
    """
    global _price_refresher

    if _price_refresher is None:
        _price_refresher = PriceRefresher()

    return _price_refresher
