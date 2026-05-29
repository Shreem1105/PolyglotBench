import os
from pathlib import Path

import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test_polyglotbench.db"

from app.db import models as db_models
from app.db.database import Base, engine

_TEST_DB_FILE = Path("test_polyglotbench.db")
if _TEST_DB_FILE.exists():
    _TEST_DB_FILE.unlink()


@pytest.fixture(scope="session", autouse=True)
def setup_and_cleanup_test_database() -> None:
    _ = db_models
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    if _TEST_DB_FILE.exists():
        _TEST_DB_FILE.unlink()
