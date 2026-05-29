from app.db.database import get_engine_kwargs


def test_get_engine_kwargs_for_sqlite() -> None:
    kwargs = get_engine_kwargs("sqlite:///./polyglotbench.db")
    assert kwargs == {"connect_args": {"check_same_thread": False}}


def test_get_engine_kwargs_for_postgresql() -> None:
    kwargs = get_engine_kwargs("postgresql://user:password@localhost:5432/polyglotbench")
    assert kwargs == {}


def test_get_engine_kwargs_for_postgresql_psycopg2() -> None:
    kwargs = get_engine_kwargs(
        "postgresql+psycopg2://user:password@localhost:5432/polyglotbench"
    )
    assert kwargs == {}
