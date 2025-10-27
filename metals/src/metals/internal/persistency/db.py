import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# TODO: echo should be dependent on whether being in development or production
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db/database.db"), echo=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to provide a database session for the request lifecycle."""
    with Session(engine) as session:
        yield session
