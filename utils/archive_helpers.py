from pathlib import Path
import subprocess

def make_7z(src_paths, out_path: Path, password: str=None):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['7z','a', str(out_path)] + [str(p) for p in src_paths]
    if password:
        cmd.insert(2, '-p' + password)
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stdout)
    return out_path
