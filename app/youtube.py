from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.models import VideoInfo


YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def extract_youtube_url(text: str) -> str | None:
    for raw in text.split():
        candidate = raw.strip("<>()[]{}.,")
        parsed = urlparse(candidate)
        host = parsed.netloc.lower()
        if host in YOUTUBE_HOSTS and parsed.scheme in {"http", "https"}:
            if host == "youtu.be" and parsed.path.strip("/"):
                return candidate
            if parse_qs(parsed.query).get("v"):
                return candidate
    return None


def download_audio(url: str, output_dir: Path, max_video_seconds: int) -> VideoInfo:
    from yt_dlp import YoutubeDL

    output_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(output_dir / "%(id)s.%(ext)s")

    with YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
        info = ydl.extract_info(url, download=False)

    duration = info.get("duration")
    if isinstance(duration, int) and duration > max_video_seconds:
        raise ValueError(f"Video is {duration}s, over the {max_video_seconds}s limit")

    options = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
    }

    with YoutubeDL(options) as ydl:
        downloaded = ydl.extract_info(url, download=True)

    video_id = downloaded["id"]
    audio_path = output_dir / f"{video_id}.mp3"
    if not audio_path.exists():
        matches = sorted(output_dir.glob(f"{video_id}.*"))
        if not matches:
            raise RuntimeError("Audio extraction finished but no audio file was found")
        audio_path = matches[0]

    return VideoInfo(
        title=str(downloaded.get("title") or "Untitled video"),
        url=url,
        duration_seconds=downloaded.get("duration") if isinstance(downloaded.get("duration"), int) else None,
        audio_path=str(audio_path),
    )
