from __future__ import annotations

MAX_TELEGRAM_MESSAGE = 3900


def split_for_telegram(text: str, max_chars: int = MAX_TELEGRAM_MESSAGE) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for line in text.splitlines(keepends=True):
        if len(line) > max_chars:
            if current:
                chunks.append("".join(current).rstrip())
                current = []
                current_len = 0
            for start in range(0, len(line), max_chars):
                chunks.append(line[start : start + max_chars].rstrip())
            continue

        if current_len + len(line) > max_chars and current:
            chunks.append("".join(current).rstrip())
            current = [line]
            current_len = len(line)
        else:
            current.append(line)
            current_len += len(line)

    if current:
        chunks.append("".join(current).rstrip())

    return [chunk for chunk in chunks if chunk]
