import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from ...routers.shared import is_development_mode

engine = create_engine(
    os.getenv("DATABASE_URL", "sqlite:///db/database.db"), echo=is_development_mode()
)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to provide a database session for the request lifecycle."""
    with Session(engine) as session:
        yield session
