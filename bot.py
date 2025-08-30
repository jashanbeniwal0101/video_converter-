# bot.py
import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Import handlers (ensure __init__.py exists in handlers/)
from handlers import (
    audio_tools,
    video_tools,
    archive_tools,
    bulk_mode,
    media_menu,
    ui_helpers,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    # Create Pyrogram bot client
    bot = Client(
        "video_converter_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="handlers")  # auto-load all handler files
    )

    logger.info("🚀 Bot starting...")

    # Start bot
    bot.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped manually")
