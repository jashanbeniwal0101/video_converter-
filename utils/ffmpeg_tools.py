import subprocess
from pathlib import Path
from typing import List

def run_cmd(cmd: list):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stdout)
    return p.stdout

def probe_format(path: Path) -> dict:
    cmd = [
        'ffprobe','-v','error','-print_format','json','-show_format','-show_streams', str(path)
    ]
    import json
    out = run_cmd(cmd)
    return json.loads(out)

def convert_video(input_path: Path, output_path: Path, vcodec='libx264', acodec='aac', crf=23, preset='medium') -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg','-y','-i', str(input_path),
        '-c:v', vcodec, '-crf', str(crf), '-preset', preset,
        '-c:a', acodec, '-movflags', '+faststart', str(output_path)
    ]
    run_cmd(cmd)
    return output_path

def extract_audio(input_path: Path, out_path: Path, codec='copy') -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-y','-i', str(input_path), '-vn', '-c:a', codec, str(out_path)]
    run_cmd(cmd)
    return out_path

def remove_audio(input_path: Path, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-y','-i', str(input_path), '-c','copy','-an', str(out_path)]
    run_cmd(cmd)
    return out_path

def trim(input_path: Path, out_path: Path, start: str, end: str=None) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-y','-ss', start]
    if end:
        cmd += ['-to', end]
    cmd += ['-i', str(input_path), '-c','copy', str(out_path)]
    run_cmd(cmd)
    return out_path

def mute_video(input_path: Path, out_path: Path) -> Path:
    return remove_audio(input_path, out_path)

def merge_videos(file_list: List[Path], out_path: Path) -> Path:
    # create a temp file list
    tf = out_path.parent / 'concat_list.txt'
    tf.write_text('
'.join(f"file '{p}'" for p in file_list))
    cmd = ['ffmpeg','-y','-f','concat','-safe','0','-i', str(tf), '-c','copy', str(out_path)]
    run_cmd(cmd)
    return out_path

def screenshot_at(input_path: Path, out_path: Path, timecode: str) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['ffmpeg','-y','-ss', timecode, '-i', str(input_path), '-frames:v','1', str(out_path)]
    run_cmd(cmd)
    return out_path

def gif_from_range(input_path: Path, out_path: Path, start: str, duration: int, fps: int=15, scale='640:-1') -> Path:
    # two-pass palette method
    pal = out_path.parent / 'palette.png'
    cmd1 = ['ffmpeg','-y','-ss', start, '-t', str(duration), '-i', str(input_path), '-vf', f'fps={fps},scale={scale},palettegen', str(pal)]
    run_cmd(cmd1)
    cmd2 = ['ffmpeg','-y','-ss', start, '-t', str(duration), '-i', str(input_path), '-i', str(pal), '-lavfi', f'fps={fps},scale={scale} [x]; [x][1:v] paletteuse', str(out_path)]
    run_cmd(cmd2)
    return out_path
