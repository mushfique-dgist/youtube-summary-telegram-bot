# YouTube summary Telegram bot

Telegram bot for summarizing YouTube videos with Whisper transcription. It accepts a YouTube URL, extracts audio, transcribes it, and returns a timestamped summary plus key takeaways.

This was built for AGuild quest #2.

## Features

- Telegram bot interface with `/start` and URL handling.
- YouTube audio extraction through `yt-dlp`.
- Whisper transcription with `faster-whisper`, including English and Chinese auto-detection.
- Timestamped sections and key takeaways.
- Optional OpenAI summarization when `OPENAI_API_KEY` is set.
- Railway-ready Dockerfile and Procfile.
- Tests for formatting, timestamp handling, Chinese text, and message chunking.

## Local setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set:

```text
TELEGRAM_BOT_TOKEN=123456:replace-me
```

Then run:

```bash
python -m app.bot
```

## Railway deployment

1. Create a new Railway project from this repo.
2. Add the variables from `.env.example`.
3. Deploy with the included `Dockerfile`.

Railway needs these variables:

```text
TELEGRAM_BOT_TOKEN=...
WHISPER_MODEL=base
MAX_VIDEO_SECONDS=1800
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_API_KEY` is optional. Without it, the bot returns an extractive summary from the transcript. With it, the bot asks the model for a tighter summary and key takeaways.

## Bot behavior

Send a YouTube URL:

```text
https://www.youtube.com/watch?v=...
```

The bot replies with:

- detected language
- video title and duration
- short summary
- timestamped sections
- key takeaways

Long replies are split into Telegram-safe chunks.

## Test

```bash
python -m pytest
python -m compileall app tests
```

The tests avoid network and external services.

## Notes

- YouTube download support depends on `yt-dlp` and the target video's availability.
- The Docker image installs `ffmpeg`, which `yt-dlp` needs for audio conversion.
- Whisper runs on CPU by default. Use `WHISPER_MODEL=tiny` for cheap hosting and `base` or `small` for better transcripts.
