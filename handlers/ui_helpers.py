from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client


def init(app: Client):
    @app.on_message()
    async def catchall(_, m):
        # lightweight help trigger
        if m.text and m.text.lower().startswith('/help'):
            await m.reply_text('This bot supports many media ops. Reply to media and use inline menu. Commands: /convert /trim /gif /extract_audio /remove_audio /zip /unzip /a_convert /slow')
