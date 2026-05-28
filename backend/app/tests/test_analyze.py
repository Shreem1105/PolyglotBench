from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_analyze_valid_request_returns_expected_fields() -> None:
    response = client.post(
        "/analyze",
        json={"text": "Hello world from PolyglotBench", "model_ids": ["gpt-4o-mini"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert "baseline_model_id" in body
    assert "analyses" in body
    assert isinstance(body["analyses"], list)
    assert len(body["analyses"]) == 1

    analysis = body["analyses"][0]
    assert "token_count" in analysis
    assert "word_count" in analysis
    assert "fertility" in analysis
    assert "fairness_score" in analysis


def test_analyze_empty_text_returns_400() -> None:
    response = client.post(
        "/analyze",
        json={"text": "   \n\t", "model_ids": ["gpt-4o-mini"]},
    )
    assert response.status_code == 400


def test_analyze_empty_model_ids_returns_400() -> None:
    response = client.post(
        "/analyze",
        json={"text": "Hello world", "model_ids": []},
    )
    assert response.status_code == 400


def test_analyze_duplicate_model_ids_returns_400() -> None:
    response = client.post(
        "/analyze",
        json={"text": "Hello world", "model_ids": ["gpt-4o-mini", "gpt-4o-mini"]},
    )
    assert response.status_code == 400


def test_analyze_unknown_model_id_returns_400() -> None:
    response = client.post(
        "/analyze",
        json={"text": "Hello world", "model_ids": ["does-not-exist"]},
    )
    assert response.status_code == 400


def test_analyze_unknown_baseline_model_id_returns_400() -> None:
    response = client.post(
        "/analyze",
        json={
            "text": "Hello world",
            "model_ids": ["gpt-4o-mini"],
            "baseline_model_id": "unknown-baseline",
        },
    )
    assert response.status_code == 400


def test_baseline_model_not_required_in_selected_model_ids() -> None:
    response = client.post(
        "/analyze",
        json={
            "text": "Hello world",
            "model_ids": ["gpt-4o"],
            "baseline_model_id": "gpt-4o-mini",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["baseline_model_id"] == "gpt-4o-mini"
    assert body["analyses"][0]["model_id"] == "gpt-4o"
