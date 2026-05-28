from functools import lru_cache

import tiktoken
from transformers import AutoTokenizer

from app.core.model_registry import get_model


@lru_cache(maxsize=16)
def _load_hf_tokenizer(tokenizer_name: str) -> AutoTokenizer:
    return AutoTokenizer.from_pretrained(tokenizer_name)


def tokenize_text(text: str, model_id: str) -> list[str]:
    model_info = get_model(model_id)
    tokenizer_type = model_info["tokenizer_type"]
    tokenizer_name = model_info["tokenizer_name"]

    if tokenizer_type == "tiktoken":
        encoding = tiktoken.get_encoding(tokenizer_name)
        token_ids = encoding.encode(text)
        return [str(token_id) for token_id in token_ids]

    if tokenizer_type == "huggingface":
        tokenizer = _load_hf_tokenizer(tokenizer_name)
        return tokenizer.tokenize(text)

    raise ValueError(
        f"Unsupported tokenizer_type '{tokenizer_type}' for model '{model_id}'."
    )


def count_tokens(text: str, model_id: str) -> int:
    return len(tokenize_text(text, model_id))
