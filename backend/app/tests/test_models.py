from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_models_endpoint_returns_starter_models() -> None:
    response = client.get("/models")
    assert response.status_code == 200

    body = response.json()
    assert "models" in body
    models = body["models"]
    assert len(models) >= 4

    model_ids = {model["id"] for model in models}
    expected = {
        "gpt-4o-mini",
        "gpt-4o",
        "bert-base-multilingual-cased",
        "xlm-roberta-base",
    }
    assert expected.issubset(model_ids)


def test_models_have_required_fields() -> None:
    response = client.get("/models")
    assert response.status_code == 200

    models = response.json()["models"]
    for model in models:
        assert "id" in model
        assert "display_name" in model
        assert "provider" in model
        assert "tokenizer_type" in model
        assert "tokenizer_name" in model
        assert "input_price_per_million_tokens" in model
        assert "notes" in model
