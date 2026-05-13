# YouTube summary Telegram bot

Telegram bot for summarizing YouTube videos with Whisper transcription. It accepts a YouTube URL, extracts audio, transcribes it, and returns a timestamped summary plus key takeaways.

This was built for AGuild quest #2.

## Features

- Telegram bot interface with `/start` and URL handling.
- YouTube audio extraction through `yt-dlp`.
- Whisper transcription with `faster-whisper`, including English and Chinese auto-detection.
- Timestamped sections and key takeaways.
- Optional OpenAI summarization when `OPENAI_API_KEY` is set.
- Railway-ready Dockerfile, Procfile, and `railway.json`.
- Tests for formatting, timestamp handling, Chinese text, and message chunking.

## Quest checklist

| AGuild deliverable | Status |
| --- | --- |
| Working Telegram bot deployed on Railway | Repo is Railway-ready. Live deployment needs the quest owner's Telegram bot token and Railway project access, or approval to deploy under a temporary bot. |
| GitHub repo with README and setup instructions | Included here. |
| Support for English and Chinese videos | Whisper language detection is enabled, and the summary builder preserves English and Chinese transcript text. |
| 2 rounds of revision included | Available after review or assignment. |

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

You can also run an offline smoke demo without Telegram, YouTube, Whisper, or OpenAI credentials:

```bash
python scripts/smoke_demo.py
```

That command prints sample English and Chinese bot replies using fixed transcript segments. It is meant for quick review of the reply format before a live token is provided.

For deployment review without exposing a real token, run:

```bash
python scripts/config_check.py --allow-missing-token
```

For live deployment, set the real environment variables and run:

```bash
python scripts/config_check.py
```

The config check validates required settings and numeric limits while masking any secrets that are present.

## Notes

- YouTube download support depends on `yt-dlp` and the target video's availability.
- The Docker image installs `ffmpeg`, which `yt-dlp` needs for audio conversion.
- Whisper runs on CPU by default. Use `WHISPER_MODEL=tiny` for cheap hosting and `base` or `small` for better transcripts.
