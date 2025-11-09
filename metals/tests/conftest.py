from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from metals.internal.persistency.db import get_session
from metals.internal.persistency.models import BaseModel
from metals.main import app


@pytest.fixture
def test_db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    BaseModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    BaseModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(test_db: Session) -> Generator[TestClient, None, None]:
    def override_get_session() -> Generator[Session, None, None]:
        yield test_db

    app.dependency_overrides[get_session] = override_get_session

    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides.clear()
