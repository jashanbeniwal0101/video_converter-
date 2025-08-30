import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
OWNER_ID = int(os.getenv('OWNER_ID', '0'))

WORKDIR = Path(os.getenv('WORKDIR', './runtime')).resolve()
WORKDIR.mkdir(parents=True, exist_ok=True)

MAX_JOBS_PER_USER = int(os.getenv('MAX_JOBS_PER_USER', '1'))
MAX_INPUT_SIZE_MB = int(os.getenv('MAX_INPUT_SIZE_MB', '4096'))

# ffmpeg tuning defaults
DEFAULT_CRf = 23
DEFAULT_PRESET = 'medium'
