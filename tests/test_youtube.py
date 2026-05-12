from app.youtube import extract_youtube_url


def test_extract_youtube_url_from_full_url() -> None:
    assert extract_youtube_url("watch this https://www.youtube.com/watch?v=abc123") == (
        "https://www.youtube.com/watch?v=abc123"
    )


def test_extract_youtube_url_from_short_url() -> None:
    assert extract_youtube_url("https://youtu.be/abc123") == "https://youtu.be/abc123"


def test_extract_youtube_url_from_short_form_paths() -> None:
    assert extract_youtube_url("https://www.youtube.com/shorts/abc123") == "https://www.youtube.com/shorts/abc123"
    assert extract_youtube_url("https://www.youtube.com/live/abc123") == "https://www.youtube.com/live/abc123"
    assert extract_youtube_url("https://www.youtube.com/embed/abc123") == "https://www.youtube.com/embed/abc123"


def test_extract_youtube_url_rejects_other_hosts() -> None:
    assert extract_youtube_url("https://example.com/watch?v=abc123") is None
