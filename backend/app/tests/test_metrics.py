from app.services.metrics_service import (
    calculate_attention_cost_multiplier,
    calculate_fairness_score,
    calculate_fertility,
    calculate_token_multiplier,
    count_characters_no_spaces,
    count_words,
)


def test_count_words() -> None:
    assert count_words("hello world from polyglotbench") == 4


def test_count_characters_no_spaces() -> None:
    assert count_characters_no_spaces("a b\tc\n") == 3


def test_calculate_fertility_normal_case() -> None:
    assert calculate_fertility(10, 5) == 2.0


def test_calculate_fertility_zero_word_case() -> None:
    assert calculate_fertility(10, 0) == 0.0


def test_calculate_token_multiplier() -> None:
    assert calculate_token_multiplier(12, 6) == 2.0


def test_calculate_attention_cost_multiplier() -> None:
    assert calculate_attention_cost_multiplier(2.0) == 4.0


def test_calculate_fairness_score_for_one() -> None:
    assert calculate_fairness_score(1.0) == 100.0


def test_calculate_fairness_score_for_two() -> None:
    assert calculate_fairness_score(2.0) == 50.0
