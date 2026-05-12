from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoInfo:
    title: str
    url: str
    duration_seconds: int | None
    audio_path: str


@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Transcript:
    language: str
    segments: list[TranscriptSegment]

    @property
    def text(self) -> str:
        return " ".join(segment.text.strip() for segment in self.segments if segment.text.strip())
