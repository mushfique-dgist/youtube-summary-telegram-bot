from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from app.config import Settings
from app.summarize import build_summary, summarize_with_openai
from app.transcribe import transcribe_audio
from app.youtube import download_audio


def process_video(url: str, settings: Settings) -> str:
    with TemporaryDirectory(dir=settings.work_dir) as temp_dir:
        video = download_audio(url, Path(temp_dir), settings.max_video_seconds)
        transcript = transcribe_audio(video.audio_path, settings.whisper_model)
        model_summary = None
        if settings.openai_api_key:
            model_summary = summarize_with_openai(transcript, settings.openai_api_key, settings.openai_model)
        return build_summary(video, transcript, model_summary)
