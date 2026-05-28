
def count_words(text: str) -> int:
    return len(text.split())


def count_characters_no_spaces(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def calculate_fertility(token_count: int, word_count: int) -> float:
    if word_count == 0:
        return 0.0
    return round(token_count / word_count, 4)


def calculate_token_multiplier(token_count: int, baseline_token_count: int) -> float:
    if baseline_token_count == 0:
        return 0.0
    return round(token_count / baseline_token_count, 4)


def calculate_attention_cost_multiplier(token_multiplier: float) -> float:
    return round(token_multiplier ** 2, 4)


def calculate_fairness_score(token_multiplier: float) -> float:
    if token_multiplier <= 0:
        return 0.0
    score = 100 / token_multiplier
    clamped = max(0.0, min(100.0, score))
    return round(clamped, 4)
