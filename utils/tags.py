from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import APIC, TIT2, TPE1, TALB
from pathlib import Path

def set_cover(file_path: Path, image_path: Path):
    audio = File(str(file_path))
    if audio is None:
        return False
    if file_path.suffix.lower() == '.mp3':
        from mutagen.easyid3 import EasyID3
        audio = MP3(str(file_path), ID3=EasyID3)
        with open(image_path, 'rb') as img:
            audio.tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=img.read()))
        audio.save()
        return True
    # other formats handled minimally
    return False
