from __future__ import annotations

import tiktoken


def count_tokens(text: str, model: str | None) -> int:
    if not text:
        return 0

    encoding = _get_encoding(model)
    return len(encoding.encode(text))


def _get_encoding(model: str | None) -> tiktoken.Encoding:
    if model:
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            pass
    return tiktoken.get_encoding("cl100k_base")
