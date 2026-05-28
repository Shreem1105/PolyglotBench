# Metrics Specification

## 1. token_count
Total number of tokens produced by a tokenizer for the given input.

`token_count = len(tokens)`

## 2. word_count
Count of words in normalized input text (language-aware tokenization rules may be improved later).

`word_count = number_of_words_in_input`

## 3. character_count_no_spaces
Total non-space characters in input text.

`character_count_no_spaces = len(input_text_without_spaces)`

## 4. fertility
Tokens per word.

`fertility = token_count / word_count`

## 5. token_multiplier
Relative token inflation against a baseline tokenizer/model.

`token_multiplier = token_count / baseline_token_count`

## 6. estimated_attention_cost_multiplier
Quadratic attention proxy based on token multiplier.

`estimated_attention_cost_multiplier = token_multiplier^2`

## 7. cost_estimate
Estimated input-side cost using published pricing.

`cost_estimate = token_count / 1_000_000 * price_per_million_tokens`

## 8. fairness_score (0 to 100)
Higher score indicates lower token inflation relative to baseline.

`fairness_score = clamp(0, 100, 100 / token_multiplier)`

Where:
- `100` is parity with baseline (`token_multiplier = 1`)
- Scores decrease as token inflation increases
- Clamp keeps the score in the `[0, 100]` range
