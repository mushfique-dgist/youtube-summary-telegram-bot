from __future__ import annotations

from app.models import Transcript, TranscriptSegment


def transcribe_audio(audio_path: str, model_name: str) -> Transcript:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments_iter, info = model.transcribe(audio_path, vad_filter=True)

    segments = [
        TranscriptSegment(start=segment.start, end=segment.end, text=segment.text.strip())
        for segment in segments_iter
        if segment.text.strip()
    ]

    return Transcript(language=info.language or "unknown", segments=segments)
