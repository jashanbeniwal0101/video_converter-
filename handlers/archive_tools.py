from pyrogram import Client, filters
from pyrogram.types import Message
from pathlib import Path
from utils.file_tools import safe_name, make_zip, unzip_first_video, clean_dir
from utils.archive_helpers import make_7z
from config import WORKDIR

JOB_PREFIX = 'job'


def init(app: Client):
    @app.on_message(filters.command('zip'))
    async def zip_cmd(client: Client, m: Message):
        if not m.reply_to_message: return await m.reply_text('Reply to file with /zip')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.audio or m.reply_to_message.video).file_name or 'file')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.zip"
        try:
            make_zip([in_file], out)
        except Exception as e:
            await m.reply_text(f'Zip failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('unzip'))
    async def unzip_cmd(client: Client, m: Message):
        if not m.reply_to_message: return await m.reply_text('Reply to a .zip with /unzip')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name(m.reply_to_message.document.file_name or 'archive.zip')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        vid = unzip_first_video(in_file, jobdir / 'extracted')
        if not vid:
            await m.reply_text('No video found in archive')
            clean_dir(jobdir)
            return
        await m.reply_document(str(vid))
        clean_dir(jobdir)

    @app.on_message(filters.command('7z'))
    async def sevenzip_cmd(client: Client, m: Message):
        # simple: reply to file to package it
        if not m.reply_to_message: return await m.reply_text('Reply to file with /7z')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'file')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.7z"
        try:
            make_7z([in_file], out)
        except Exception as e:
            await m.reply_text(f'7z failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)
