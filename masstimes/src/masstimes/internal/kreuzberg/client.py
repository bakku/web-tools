import logging

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def fetch_kreuzberg_pdf_url() -> str | None:
    async with httpx.AsyncClient() as client:
        logger.info("Starting to fetch Kreuzberg PDF.")

        response = await client.get("https://www.kreuzberg-schwandorf.de/pfarrbrief/")

        if response.status_code != 200:
            logger.info(
                f"Got unexpected status code: {response.status_code}. Returning None."
            )
            return None

        doc = BeautifulSoup(response.text, "html.parser")

        elements = [
            a for a in doc.find_all("a") if a.string == "Pfarrbrief herunterladen"
        ]

        if len(elements) > 1:
            logger.info(
                f"Found {len(elements)} possible candidates for PDF URL. "
                f"Returning None."
            )
            return None

        if len(elements) == 0:
            logger.info("Found no possible candidate for PDF URL. Returning None.")
            return None

        logger.info("Successfully fetched Kreuzberg PDF URL.")

        return str(elements[0]["href"])
