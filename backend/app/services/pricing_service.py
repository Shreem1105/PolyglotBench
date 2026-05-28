
def calculate_input_cost(token_count: int, price_per_million_tokens: float) -> float:
    cost = (token_count / 1_000_000) * price_per_million_tokens
    return round(cost, 8)
