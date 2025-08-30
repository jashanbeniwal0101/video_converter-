from pyrogram import Client, filters
from pyrogram.types import Message
from pathlib import Path
from config import WORKDIR, DEFAULT_CRf, DEFAULT_PRESET
from utils.file_tools import safe_name, clean_dir
from utils.ffmpeg_tools import convert_video, extract_audio, remove_audio, trim, merge_videos, screenshot_at, gif_from_range
from utils.file_tools import ALLOWED_VIDEO_EXT
from utils.file_tools import make_zip
from datetime import datetime

JOB_PREFIX = 'job'


def init(app: Client):
    @app.on_message(filters.command('convert'))
    async def convert_cmd(client: Client, m: Message):
        if not m.reply_to_message or not (m.reply_to_message.video or m.reply_to_message.document):
            return await m.reply_text('Reply to a video/document with `/convert mp4`')
        parts = (m.text or '').split()
        fmt = parts[1] if len(parts) > 1 else 'mp4'
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}_{int(datetime.utcnow().timestamp())}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out_file = jobdir / f"{in_file.stem}.{fmt}"
        try:
            convert_video(in_file, out_file, crf=DEFAULT_CRf, preset=DEFAULT_PRESET)
        except Exception as e:
            await m.reply_text(f'Conversion failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out_file), caption=f'Converted to {fmt}')
        clean_dir(jobdir)

    @app.on_message(filters.command('extract_audio'))
    async def extract_audio_cmd(client: Client, m: Message):
        if not m.reply_to_message: return await m.reply_text('Reply to a video with /extract_audio')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.m4a"
        try:
            extract_audio(in_file, out, codec='aac')
        except Exception as e:
            await m.reply_text(f'Extraction failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_audio(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('remove_audio') | filters.command('mute'))
    async def remove_audio_cmd(client: Client, m: Message):
        if not m.reply_to_message: return await m.reply_text('Reply to a video with /remove_audio')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.muted{in_file.suffix}"
        try:
            remove_audio(in_file, out)
        except Exception as e:
            await m.reply_text(f'Failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('trim'))
    async def trim_cmd(client: Client, m: Message):
        # usage: /trim start=00:01:00 end=00:02:00
        text = m.text or ''
        if not m.reply_to_message: return await m.reply_text('Reply to a video with /trim start=.. end=..')
        def parse_param(key):
            for part in text.split():
                if part.startswith(key+'='):
                    return part.split('=',1)[1]
            return None
        start = parse_param('start')
        end = parse_param('end')
        if not start: return await m.reply_text('Provide start time e.g. start=00:00:10')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.trim{in_file.suffix}"
        try:
            trim(in_file, out, start, end)
        except Exception as e:
            await m.reply_text(f'Trim failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('screenshot'))
    async def screenshot_cmd(client: Client, m: Message):
        # usage: /screenshot time=00:00:10
        text = m.text or ''
        if not m.reply_to_message: return await m.reply_text('Reply to a video with /screenshot time=HH:MM:SS')
        time = None
        for part in text.split():
            if part.startswith('time='):
                time = part.split('=',1)[1]
        if time is None:
            return await m.reply_text('Provide time=HH:MM:SS')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.{time.replace(':','-')}.jpg"
        try:
            screenshot_at(in_file, out, time)
        except Exception as e:
            await m.reply_text(f'Failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_photo(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('gif'))
    async def gif_cmd(client: Client, m: Message):
        # /gif start=00:00:10 dur=5
        text = m.text or ''
        if not m.reply_to_message: return await m.reply_text('Reply to a video with /gif start=.. dur=..')
        start = None; dur = None
        for part in text.split():
            if part.startswith('start='): start = part.split('=',1)[1]
            if part.startswith('dur='): dur = int(part.split('=',1)[1])
        if not start or not dur: return await m.reply_text('Provide start and dur')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.video).file_name or 'video')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.gif"
        try:
            gif_from_range(in_file, out, start, dur)
        except Exception as e:
            await m.reply_text(f'GIF failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)
