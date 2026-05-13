from __future__ import annotations

import re
from collections import Counter

from app.models import Transcript, TranscriptSegment, VideoInfo


STOPWORDS = {
    "a",
    "about",
    "and",
    "are",
    "for",
    "from",
    "have",
    "that",
    "the",
    "this",
    "with",
    "you",
    "your",
    "了",
    "在",
    "是",
    "我",
    "有",
    "和",
    "的",
}


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    minutes, sec = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{sec:02d}"
    return f"{minutes}:{sec:02d}"


def build_summary(video: VideoInfo, transcript: Transcript, model_summary: str | None = None) -> str:
    sections = _build_sections(transcript.segments)
    takeaways = _extract_takeaways(transcript.segments)
    duration = format_timestamp(video.duration_seconds or 0) if video.duration_seconds else "unknown"

    lines = [
        f"Video: {video.title}",
        f"Duration: {duration}",
        f"Detected language: {transcript.language}",
        "",
        "Summary",
        model_summary.strip() if model_summary else _extractive_summary(transcript.segments),
        "",
        "Timestamped sections",
    ]

    lines.extend(f"- {timestamp}: {text}" for timestamp, text in sections)
    lines.extend(["", "Key takeaways"])
    lines.extend(f"- {item}" for item in takeaways)
    return "\n".join(lines).strip()


def summarize_with_openai(transcript: Transcript, api_key: str, model: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    transcript_text = "\n".join(
        f"[{format_timestamp(segment.start)}] {segment.text}" for segment in transcript.segments
    )
    prompt = (
        "Summarize this transcript for a Telegram user. Keep it compact. "
        "Include the main argument, useful details, and any decisions or instructions. "
        "Preserve technical terms and support both English and Chinese.\n\n"
        f"{transcript_text[:24000]}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You summarize transcripts into concise Telegram messages.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return (response.choices[0].message.content or "").strip()


def _build_sections(segments: list[TranscriptSegment]) -> list[tuple[str, str]]:
    if not segments:
        return [("0:00", "No transcript content was detected.")]

    section_count = min(8, max(3, len(segments) // 8 or 1))
    stride = max(1, len(segments) // section_count)
    sections: list[tuple[str, str]] = []

    for index in range(0, len(segments), stride):
        segment = segments[index]
        text = _clean_sentence(segment.text)
        if text:
            sections.append((format_timestamp(segment.start), text))
        if len(sections) >= 8:
            break

    return sections or [("0:00", "Transcript contained no usable sections.")]


def _extractive_summary(segments: list[TranscriptSegment]) -> str:
    text = " ".join(_clean_sentence(segment.text) for segment in segments[:6])
    if not text:
        return "No transcript content was detected."
    return _limit_words(text, 90)


def _extract_takeaways(segments: list[TranscriptSegment]) -> list[str]:
    text = " ".join(_clean_sentence(segment.text) for segment in segments)
    if _has_cjk(text):
        takeaways = [_limit_chars(_clean_sentence(segment.text), 80) for segment in segments[:3]]
        return [item for item in takeaways if item] or ["文字稿太短，无法提取明确重点。"]

    words = [
        word.lower()
        for word in re.findall(r"[A-Za-z][A-Za-z0-9_'-]{2,}|[\u4e00-\u9fff]", text)
        if word.lower() not in STOPWORDS
    ]
    common = [word for word, _count in Counter(words).most_common(6)]

    if not common:
        return ["The transcript was too short to extract strong takeaways."]

    joined = ", ".join(common[:4])
    return [
        f"Main recurring terms: {joined}.",
        "Review the timestamped sections for the parts most likely to need follow-up.",
    ]


def _clean_sentence(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip(" -\t\n")


def _limit_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(".,") + "..."


def _limit_chars(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rstrip("，。,. ") + "..."


def _has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))
