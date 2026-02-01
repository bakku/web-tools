import logging
import os

from mistralai import (
    DocumentURLChunk,
    Mistral,
    TextChunk,
    UserMessage,
)

from masstimes.internal.kreuzberg.types import KreuzbergEvents

logger = logging.getLogger(__name__)


async def extract_kreuzberg_masstimes(url: str) -> KreuzbergEvents | None:
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-medium-latest"

    async with Mistral(api_key=api_key) as mistral:
        messages = [
            UserMessage(
                content=[
                    TextChunk(
                        text='Angefangen ab dem Titel "Gottesdienste", extrahiere für mich '
                        "alle Termine die in der Kirche stattfinden. Organisiere das"
                        "Resultat nach den zwei Kirchen (Kreuzberg und St. Paul). "
                        "Für jedes Event möchte ich das Datum, Uhrzeit sowie die"
                        "Beschreibung."
                    ),
                    DocumentURLChunk(document_url=url),
                ],
            )
        ]

        logger.info("Sending kreuzberg PDF request to Mistral.")

        chat_response = mistral.chat.parse(
            model=model, messages=messages, response_format=KreuzbergEvents
        )

        if chat_response.choices is None or chat_response.choices[0].message is None:
            logger.info("Could not get response from mistral.")
            return None

        logger.info(
            f"Got response for kreuzberg PDF from mistral: "
            f"{chat_response.choices[0].message.parsed}"
        )

        return chat_response.choices[0].message.parsed
