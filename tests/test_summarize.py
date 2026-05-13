from app.models import Transcript, TranscriptSegment, VideoInfo
from app.summarize import build_summary, format_timestamp


def test_format_timestamp() -> None:
    assert format_timestamp(0) == "0:00"
    assert format_timestamp(65) == "1:05"
    assert format_timestamp(3661) == "1:01:01"


def test_build_summary_keeps_chinese_text() -> None:
    video = VideoInfo(title="Chinese sample", url="https://youtu.be/example", duration_seconds=70, audio_path="x.mp3")
    transcript = Transcript(
        language="zh",
        segments=[
            TranscriptSegment(start=0, end=10, text="今天我们介绍一个自动化工作流。"),
            TranscriptSegment(start=10, end=20, text="它会下载视频并生成摘要。"),
            TranscriptSegment(start=20, end=30, text="最后输出时间戳和重点。"),
        ],
    )

    summary = build_summary(video, transcript)

    assert "Detected language: zh" in summary
    assert "今天我们介绍" in summary
    assert "Timestamped sections" in summary
    assert "Key takeaways" in summary
    assert "- 今天我们介绍一个自动化工作流。" in summary


def test_build_summary_uses_model_summary_when_present() -> None:
    video = VideoInfo(title="English sample", url="https://youtu.be/example", duration_seconds=120, audio_path="x.mp3")
    transcript = Transcript(
        language="en",
        segments=[
            TranscriptSegment(start=0, end=10, text="This video explains a Telegram bot architecture."),
            TranscriptSegment(start=10, end=20, text="The bot downloads audio and transcribes it."),
        ],
    )

    summary = build_summary(video, transcript, model_summary="A compact model-written summary.")

    assert "A compact model-written summary." in summary
    assert "- 0:00:" in summary
