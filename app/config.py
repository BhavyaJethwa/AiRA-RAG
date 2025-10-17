import os
from dotenv import load_dotenv
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
SQLITE_URL = os.getenv("SQLITE_URL", "sqlite+aiosqlite:///./metadata.db")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-large")
