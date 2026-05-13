import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

DB_DSN = os.getenv("DB_DSN")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")