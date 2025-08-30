import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import media_menu, video_tools, audio_tools, archive_tools, ui_helpers, bulk_mode

app = Client('media-bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# register handlers
media_menu.init(app)
video_tools.init(app)
audio_tools.init(app)
archive_tools.init(app)
ui_helpers.init(app)
bulk_mode.init(app)

if __name__ == '__main__':
    print('Bot starting...')
    app.run()
