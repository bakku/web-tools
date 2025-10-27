import os

from sqlalchemy import create_engine

# TODO: echo should be dependent on whether being in development or production
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///db/database.db"), echo=True)
