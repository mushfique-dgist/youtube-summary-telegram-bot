from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    whisper_model: str
    max_video_seconds: int
    openai_api_key: str | None
    openai_model: str
    work_dir: Path


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    max_video_seconds = int(os.getenv("MAX_VIDEO_SECONDS", "1800"))
    if max_video_seconds <= 0:
        raise RuntimeError("MAX_VIDEO_SECONDS must be positive")

    work_dir = Path(os.getenv("WORK_DIR", "/tmp/youtube-summary-bot"))
    work_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        telegram_bot_token=token,
        whisper_model=os.getenv("WHISPER_MODEL", "base").strip() or "base",
        max_video_seconds=max_video_seconds,
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip() or None,
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
        work_dir=work_dir,
    )
