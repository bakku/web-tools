from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.orm import Session

from masstimes.internal.kreuzberg.client import fetch_kreuzberg_pdf_url
from masstimes.internal.kreuzberg.llm import extract_kreuzberg_masstimes
from masstimes.internal.persistency.db import get_session
from masstimes.internal.persistency.models import Event
from masstimes.internal.types import Church

router = APIRouter()


@router.post("/jobs")
async def admin_post_jobs(
    request: Request,
    session: Annotated[Session, Depends(get_session)],
) -> Response:
    pdf_url = await fetch_kreuzberg_pdf_url()

    if pdf_url is None:
        # For now, we just return bad request. Should be improved later.
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    result = await extract_kreuzberg_masstimes(pdf_url)

    if result is None:
        # For now, we just return bad request. Should be improved later.
        return Response(status_code=status.HTTP_400_BAD_REQUEST)

    for event in result.events:
        new_event = Event(
            church=Church.KREUZBERG if event.church == "Kreuzberg" else Church.ST_PAUL,
            occurring_at=event.time,
            description=event.description,
        )

        session.add(new_event)

    session.commit()

    return RedirectResponse(
        url=request.url_for("admin_get_home"), status_code=status.HTTP_303_SEE_OTHER
    )
