from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import Transcript, TranscriptSegment, VideoInfo
from app.summarize import build_summary


def build_demo_outputs() -> dict[str, str]:
    return {
        "English demo": english_demo(),
        "Chinese demo": chinese_demo(),
    }


def english_demo() -> str:
    video = VideoInfo(
        title="Demo: shipping a Telegram summary bot",
        url="https://youtu.be/demo",
        duration_seconds=145,
        audio_path="demo.mp3",
    )
    transcript = Transcript(
        language="en",
        segments=[
            TranscriptSegment(0, 18, "This walkthrough explains how a Telegram bot accepts a YouTube URL."),
            TranscriptSegment(18, 41, "The bot extracts audio with yt-dlp and sends it to Whisper for transcription."),
            TranscriptSegment(41, 76, "The summary includes timestamps so the reader can jump back to the source video."),
            TranscriptSegment(76, 120, "Railway deployment only needs the Telegram bot token and the environment variables."),
        ],
    )
    return build_summary(video, transcript)


def chinese_demo() -> str:
    video = VideoInfo(
        title="演示：中文视频摘要",
        url="https://youtu.be/demo-zh",
        duration_seconds=98,
        audio_path="demo-zh.mp3",
    )
    transcript = Transcript(
        language="zh",
        segments=[
            TranscriptSegment(0, 16, "这个视频介绍如何把 YouTube 链接发给 Telegram 机器人。"),
            TranscriptSegment(16, 39, "机器人会下载音频，使用 Whisper 生成文字稿。"),
            TranscriptSegment(39, 70, "最后回复带时间戳的摘要和重点，方便用户快速回看。"),
        ],
    )
    return build_summary(video, transcript)


def main() -> None:
    for index, (title, output) in enumerate(build_demo_outputs().items()):
        if index:
            print()
        print(f"=== {title} ===")
        print(output)


if __name__ == "__main__":
    main()
