from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_submission_from_analysis_returns_created() -> None:
    response = client.post(
        "/submissions/from-analysis",
        json={
            "text": "Artificial intelligence helps teams build software faster.",
            "model_ids": ["gpt-4o-mini"],
        },
    )

    assert response.status_code in (200, 201)
    body = response.json()
    assert "id" in body
    assert "language_detected" in body
    assert isinstance(body["selected_models"], list)
    assert body["selected_models"] == ["gpt-4o-mini"]


def test_get_submissions_returns_list() -> None:
    response = client.get("/submissions")
    assert response.status_code == 200
    body = response.json()
    assert "submissions" in body
    assert isinstance(body["submissions"], list)


def test_create_submission_empty_text_returns_400() -> None:
    response = client.post(
        "/submissions/from-analysis",
        json={
            "text": "   \n\t",
            "model_ids": ["gpt-4o-mini"],
        },
    )
    assert response.status_code == 400


def test_create_submission_invalid_model_id_returns_400() -> None:
    response = client.post(
        "/submissions/from-analysis",
        json={
            "text": "Hello world",
            "model_ids": ["not-a-real-model"],
        },
    )
    assert response.status_code == 400
