import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv('API_ID', '25331263'))
API_HASH = os.getenv('API_HASH', 'cab85305bf85125a2ac053210bcd1030')
BOT_TOKEN = os.getenv('BOT_TOKEN', '7368321164:AAFNU9jp-x1qsb_s6VviTpiMRxkVHKwDHB4')
OWNER_ID = int(os.getenv('OWNER_ID', '1955406483'))

WORKDIR = Path(os.getenv('WORKDIR', './runtime')).resolve()
WORKDIR.mkdir(parents=True, exist_ok=True)

MAX_JOBS_PER_USER = int(os.getenv('MAX_JOBS_PER_USER', '1'))
MAX_INPUT_SIZE_MB = int(os.getenv('MAX_INPUT_SIZE_MB', '4096'))

# ffmpeg tuning defaults
DEFAULT_CRf = 23
DEFAULT_PRESET = 'medium'
