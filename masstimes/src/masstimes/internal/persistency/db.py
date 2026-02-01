import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from masstimes.utils import is_development_env

engine = create_engine(
    os.getenv("DATABASE_URL", "sqlite:///db/database.db"), echo=is_development_env()
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
