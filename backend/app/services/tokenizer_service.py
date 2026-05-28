import tiktoken
from transformers import AutoTokenizer

from app.core.model_registry import get_model

_TIKTOKEN_CACHE: dict[str, object] = {}
_HF_TOKENIZER_CACHE: dict[str, object] = {}


def _get_tiktoken_encoding(tokenizer_name: str, model_id: str) -> object:
    encoding = _TIKTOKEN_CACHE.get(tokenizer_name)
    if encoding is None:
        try:
            encoding = tiktoken.get_encoding(tokenizer_name)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load tokenizer for model '{model_id}' "
                f"(tokenizer_name='{tokenizer_name}')."
            ) from exc
        _TIKTOKEN_CACHE[tokenizer_name] = encoding
    return encoding


def _get_hf_tokenizer(tokenizer_name: str, model_id: str) -> object:
    tokenizer = _HF_TOKENIZER_CACHE.get(tokenizer_name)
    if tokenizer is None:
        try:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load tokenizer for model '{model_id}' "
                f"(tokenizer_name='{tokenizer_name}')."
            ) from exc
        _HF_TOKENIZER_CACHE[tokenizer_name] = tokenizer
    return tokenizer


def tokenize_text(text: str, model_id: str) -> list[str]:
    model_info = get_model(model_id)
    tokenizer_type = model_info["tokenizer_type"]
    tokenizer_name = model_info["tokenizer_name"]

    if tokenizer_type == "tiktoken":
        encoding = _get_tiktoken_encoding(tokenizer_name, model_id)
        try:
            token_ids = encoding.encode(text)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to tokenize text for model '{model_id}' "
                f"(tokenizer_name='{tokenizer_name}')."
            ) from exc
        return [str(token_id) for token_id in token_ids]

    if tokenizer_type == "huggingface":
        tokenizer = _get_hf_tokenizer(tokenizer_name, model_id)
        try:
            return tokenizer.tokenize(text)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to tokenize text for model '{model_id}' "
                f"(tokenizer_name='{tokenizer_name}')."
            ) from exc

    raise ValueError(
        f"Unsupported tokenizer_type '{tokenizer_type}' for model '{model_id}'."
    )


def count_tokens(text: str, model_id: str) -> int:
    return len(tokenize_text(text, model_id))
