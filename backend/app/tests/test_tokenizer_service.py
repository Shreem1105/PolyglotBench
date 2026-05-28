from app.services.tokenizer_service import count_tokens


def test_count_tokens_returns_positive_integer_for_gpt4o_mini() -> None:
    token_count = count_tokens("Hello world", "gpt-4o-mini")
    assert isinstance(token_count, int)
    assert token_count > 0
