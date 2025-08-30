from pathlib import Path
import shutil, zipfile

ALLOWED_VIDEO_EXT = {'.mp4','.mkv','.webm','.avi','.mov','.m4v'}
ALLOWED_AUDIO_EXT = {'.mp3','.m4a','.aac','.wav','.flac','.ogg','.opus'}

def safe_name(name: str) -> str:
    return ''.join(c for c in name if c.isalnum() or c in (' ','.','_','-')).strip() or 'file'

def make_zip(src_paths, out_zip: Path, password: str=None) -> Path:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if password:
        # use 7z for password support
        import subprocess
        cmd = ['7z','a','-p' + password, str(out_zip)] + [str(p) for p in src_paths]
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if r.returncode != 0:
            raise RuntimeError(r.stdout)
        return out_zip
    else:
        with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for p in src_paths:
                zf.write(p, arcname=p.name)
        return out_zip

def unzip_first_video(zip_path: Path, extract_to: Path):
    extract_to.mkdir(parents=True, exist_ok=True)
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(path=extract_to)
    for p in extract_to.rglob('*'):
        if p.suffix.lower() in ALLOWED_VIDEO_EXT:
            return p
    return None

def clean_dir(p: Path):
    try:
        if p.exists():
            shutil.rmtree(p)
    except Exception:
        pass
