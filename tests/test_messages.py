from app.messages import split_for_telegram


def test_split_for_telegram_keeps_short_message() -> None:
    assert split_for_telegram("short") == ["short"]


def test_split_for_telegram_splits_on_lines() -> None:
    text = "one\n" * 20
    chunks = split_for_telegram(text, max_chars=15)
    assert len(chunks) > 1
    assert all(len(chunk) <= 15 for chunk in chunks)
