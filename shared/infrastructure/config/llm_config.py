import os


def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


LLM_MODEL = os.getenv("LLM_MODEL")
MAX_PROMPT_TOKENS = _get_int_env("MAX_PROMPT_TOKENS", 1024)
