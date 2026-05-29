from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "polyglotbench-backend"


def test_ready_endpoint_returns_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["database"] == "ok"
    assert body["service"] == "polyglotbench-backend"


def test_root_endpoint_returns_running() -> None:
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "PolyglotBench API"
    assert body["version"] == "0.1.0"
    assert body["status"] == "running"


def test_cors_preflight_allows_frontend_origin() -> None:
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code in {200, 204}
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
