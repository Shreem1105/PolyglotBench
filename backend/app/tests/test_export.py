from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_export_json_returns_200_and_payload() -> None:
    response = client.post(
        "/export",
        json={
            "text": "Hello world from export endpoint",
            "model_ids": ["gpt-4o-mini"],
            "format": "json",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["project"] == "PolyglotBench"
    assert "analyses" in body
    assert isinstance(body["analyses"], list)


def test_export_csv_returns_200_and_csv_content() -> None:
    response = client.post(
        "/export",
        json={
            "text": "Hello world from export endpoint",
            "model_ids": ["gpt-4o-mini"],
            "format": "csv",
        },
    )

    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "attachment; filename=\"polyglotbench_export.csv\"" == response.headers.get(
        "content-disposition", ""
    )
    body = response.text
    assert "model_id" in body
    assert "fairness_score" in body


def test_export_empty_text_returns_400() -> None:
    response = client.post(
        "/export",
        json={"text": "   \n\t", "model_ids": ["gpt-4o-mini"], "format": "json"},
    )
    assert response.status_code == 400


def test_export_empty_model_ids_returns_400() -> None:
    response = client.post(
        "/export",
        json={"text": "Hello world", "model_ids": [], "format": "json"},
    )
    assert response.status_code == 400


def test_export_duplicate_model_ids_returns_400() -> None:
    response = client.post(
        "/export",
        json={
            "text": "Hello world",
            "model_ids": ["gpt-4o-mini", "gpt-4o-mini"],
            "format": "json",
        },
    )
    assert response.status_code == 400


def test_export_invalid_format_returns_400() -> None:
    response = client.post(
        "/export",
        json={"text": "Hello world", "model_ids": ["gpt-4o-mini"], "format": "xml"},
    )
    assert response.status_code == 400


def test_export_unknown_model_id_returns_400() -> None:
    response = client.post(
        "/export",
        json={"text": "Hello world", "model_ids": ["unknown-model"], "format": "json"},
    )
    assert response.status_code == 400


def test_export_unknown_baseline_model_id_returns_400() -> None:
    response = client.post(
        "/export",
        json={
            "text": "Hello world",
            "model_ids": ["gpt-4o-mini"],
            "baseline_model_id": "unknown-baseline",
            "format": "json",
        },
    )
    assert response.status_code == 400
