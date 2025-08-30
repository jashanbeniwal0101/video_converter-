from pyrogram import Client, filters
from pyrogram.types import Message
from pathlib import Path
from utils.file_tools import safe_name, clean_dir
from utils.ffmpeg_tools import extract_audio, run_cmd
from config import WORKDIR

JOB_PREFIX = 'job'


def init(app: Client):
    @app.on_message(filters.command('a_convert'))
    async def aconvert(client: Client, m: Message):
        # /a_convert mp3 192k
        parts = (m.text or '').split()
        if len(parts) < 2: return await m.reply_text('Usage: /a_convert mp3 192k')
        fmt = parts[1]
        br = parts[2] if len(parts) > 2 else '192k'
        if not m.reply_to_message: return await m.reply_text('Reply to audio or video')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.audio or m.reply_to_message.video).file_name or 'audio')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.{fmt}"
        try:
            cmd = ['ffmpeg','-y','-i', str(in_file), '-vn', '-c:a']
            if fmt == 'mp3':
                cmd += ['libmp3lame','-b:a', br, str(out)]
            elif fmt in ('m4a','aac'):
                cmd += ['aac','-b:a', br, str(out)]
            else:
                cmd += ['copy', str(out)]
            run_cmd(cmd)
        except Exception as e:
            await m.reply_text(f'Failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_document(str(out))
        clean_dir(jobdir)

    @app.on_message(filters.command('slow'))
    async def slow_effect(client: Client, m: Message):
        # /slow 75 (percent)
        parts = (m.text or '').split()
        percent = int(parts[1]) if len(parts) > 1 else 75
        if not m.reply_to_message: return await m.reply_text('Reply to audio')
        jobdir = WORKDIR / f"{JOB_PREFIX}_{m.chat.id}_{m.id}"
        jobdir.mkdir(parents=True, exist_ok=True)
        in_file = jobdir / safe_name((m.reply_to_message.document or m.reply_to_message.audio).file_name or 'audio')
        await client.download_media(m.reply_to_message, file_name=str(in_file))
        out = jobdir / f"{in_file.stem}.slow{in_file.suffix}"
        try:
            rate = percent / 100.0
            # atempo only supports 0.5-2.0; if outside chain filters needed
            if 0.5 <= rate <= 2.0:
                cmd = ['ffmpeg','-y','-i', str(in_file), '-filter:a', f'atempo={rate}', str(out)]
            else:
                # fallback: change sample rate
                cmd = ['ffmpeg','-y','-i', str(in_file), '-filter:a', f'asetrate=44100*{rate},aresample=44100', str(out)]
            run_cmd(cmd)
        except Exception as e:
            await m.reply_text(f'Failed: {e}')
            clean_dir(jobdir)
            return
        await m.reply_audio(str(out))
        clean_dir(jobdir)
