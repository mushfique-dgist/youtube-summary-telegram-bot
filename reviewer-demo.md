# Reviewer demo

These are static sample replies generated from the same summary renderer used by the Telegram bot. They do not require a Telegram token, Railway project, YouTube download, Whisper model, or OpenAI key.

To regenerate:

```bash
python scripts/smoke_demo.py
```

## English demo

```text
Video: Demo: shipping a Telegram summary bot
Duration: 2:25
Detected language: en

Summary
This walkthrough explains how a Telegram bot accepts a YouTube URL. The bot extracts audio with yt-dlp and sends it to Whisper for transcription. The summary includes timestamps so the reader can jump back to the source video. Railway deployment only needs the Telegram bot token and the environment variables.

Timestamped sections
- 0:00: This walkthrough explains how a Telegram bot accepts a YouTube URL.
- 0:18: The bot extracts audio with yt-dlp and sends it to Whisper for transcription.
- 0:41: The summary includes timestamps so the reader can jump back to the source video.
- 1:16: Railway deployment only needs the Telegram bot token and the environment variables.

Key takeaways
- Main recurring terms: bot, telegram, walkthrough, explains.
- Review the timestamped sections for the parts most likely to need follow-up.
```

## Chinese demo

```text
Video: 演示：中文视频摘要
Duration: 1:38
Detected language: zh

Summary
这个视频介绍如何把 YouTube 链接发给 Telegram 机器人。 机器人会下载音频，使用 Whisper 生成文字稿。 最后回复带时间戳的摘要和重点，方便用户快速回看。

Timestamped sections
- 0:00: 这个视频介绍如何把 YouTube 链接发给 Telegram 机器人。
- 0:16: 机器人会下载音频，使用 Whisper 生成文字稿。
- 0:39: 最后回复带时间戳的摘要和重点，方便用户快速回看。

Key takeaways
- 这个视频介绍如何把 YouTube 链接发给 Telegram 机器人。
- 机器人会下载音频，使用 Whisper 生成文字稿。
- 最后回复带时间戳的摘要和重点，方便用户快速回看。
```
