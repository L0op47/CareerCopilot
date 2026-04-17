from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
MODEL = os.getenv("DASHSCOPE_MODEL", "qwen3.6-plus")
BASE_URL = os.getenv("DASHSCOPE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True,exist_ok=True)


DATABASE_URL = "sqlite:///./resume.db"
