from __future__ import annotations

import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import load_settings
from app.messages import split_for_telegram
from app.pipeline import process_video
from app.youtube import extract_youtube_url


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
LOGGER = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    await update.effective_message.reply_text(
        "Send me a YouTube URL. I will transcribe it and return a timestamped summary."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = context.application.bot_data["settings"]
    text = update.effective_message.text or ""
    url = extract_youtube_url(text)

    if not url:
        await update.effective_message.reply_text("Send a valid YouTube URL.")
        return

    status = await update.effective_message.reply_text("Working on it. This can take a few minutes.")

    try:
        summary = await asyncio.to_thread(process_video, url, settings)
    except ValueError as exc:
        await status.edit_text(str(exc))
        return
    except Exception:
        LOGGER.exception("Video processing failed")
        await status.edit_text("I could not process that video. Check the URL or try a shorter clip.")
        return

    await status.delete()
    for chunk in split_for_telegram(summary):
        await update.effective_message.reply_text(chunk, disable_web_page_preview=True)


def main() -> None:
    settings = load_settings()
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.bot_data["settings"] = settings
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
