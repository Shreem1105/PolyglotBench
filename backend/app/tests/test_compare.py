from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_compare_with_two_texts_returns_200() -> None:
    response = client.post(
        "/compare",
        json={
            "texts": ["Hello world", "Bonjour le monde"],
            "model_ids": ["gpt-4o-mini"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total_texts"] == 2
    assert len(body["results"]) == 2
    assert "analyses" in body["results"][0]
    assert isinstance(body["results"][0]["analyses"], list)


def test_compare_empty_texts_returns_400() -> None:
    response = client.post(
        "/compare",
        json={"texts": [], "model_ids": ["gpt-4o-mini"]},
    )
    assert response.status_code == 400


def test_compare_whitespace_text_returns_400() -> None:
    response = client.post(
        "/compare",
        json={"texts": ["ok", "   \n\t"], "model_ids": ["gpt-4o-mini"]},
    )
    assert response.status_code == 400


def test_compare_empty_model_ids_returns_400() -> None:
    response = client.post(
        "/compare",
        json={"texts": ["Hello world"], "model_ids": []},
    )
    assert response.status_code == 400


def test_compare_duplicate_model_ids_returns_400() -> None:
    response = client.post(
        "/compare",
        json={"texts": ["Hello world"], "model_ids": ["gpt-4o-mini", "gpt-4o-mini"]},
    )
    assert response.status_code == 400


def test_compare_unknown_model_id_returns_400() -> None:
    response = client.post(
        "/compare",
        json={"texts": ["Hello world"], "model_ids": ["unknown-model"]},
    )
    assert response.status_code == 400


def test_compare_unknown_baseline_model_id_returns_400() -> None:
    response = client.post(
        "/compare",
        json={
            "texts": ["Hello world"],
            "model_ids": ["gpt-4o-mini"],
            "baseline_model_id": "unknown-baseline",
        },
    )
    assert response.status_code == 400


def test_compare_baseline_not_required_in_model_ids() -> None:
    response = client.post(
        "/compare",
        json={
            "texts": ["Hello world"],
            "model_ids": ["gpt-4o"],
            "baseline_model_id": "gpt-4o-mini",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["baseline_model_id"] == "gpt-4o-mini"
    assert body["results"][0]["analyses"][0]["model_id"] == "gpt-4o"
