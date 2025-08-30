from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram import Client
from utils.file_tools import safe_name

VIDEO_KEYS = [
    [InlineKeyboardButton('Convert', callback_data='video_convert')],
    [InlineKeyboardButton('Trim', callback_data='video_trim'), InlineKeyboardButton('Split', callback_data='video_split')],
    [InlineKeyboardButton('Extract Audio', callback_data='video_extract_audio'), InlineKeyboardButton('Remove Audio', callback_data='video_remove_audio')],
    [InlineKeyboardButton('Screenshots', callback_data='video_screenshots'), InlineKeyboardButton('GIF', callback_data='video_gif')],
]

AUDIO_KEYS = [[InlineKeyboardButton('Convert', callback_data='audio_convert'), InlineKeyboardButton('Effects', callback_data='audio_effects')]]

DOC_KEYS = [[InlineKeyboardButton('Rename', callback_data='doc_rename'), InlineKeyboardButton('Archive', callback_data='doc_archive')]]


def init(app: Client):
    @app.on_message(filters.media & ~filters.edited)
    async def incoming_media(_, m: Message):
        # Build menu based on media type
        kb = None
        if m.video or m.document and (m.document.file_name and m.document.file_name.split('.')[-1].lower() in ['mp4','mkv','m4v']):
            kb = InlineKeyboardMarkup(VIDEO_KEYS)
        elif m.audio or (m.document and m.document.file_name and m.document.file_name.split('.')[-1].lower() in ['mp3','m4a','wav']):
            kb = InlineKeyboardMarkup(AUDIO_KEYS)
        elif m.document:
            kb = InlineKeyboardMarkup(DOC_KEYS)
        if kb:
            await m.reply_text('Select an action from the menu below:', reply_markup=kb)

    @app.on_message(filters.command('start'))
    async def start(_, m: Message):
        await m.reply_text('Hi — send me media and use the inline menu to pick actions. Use /help for details.')
