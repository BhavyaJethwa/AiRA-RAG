import asyncio
from app.celery_app import celery_app
from app.config import CHROMA_DIR, OPENAI_API_KEY, EMBED_MODEL
from app.utils.loader import load_and_chunk_url
from app.db import AsyncSessionLocal, init_db
from app.models import Source
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def ingest_url_task(self, source_id: int, url: str):
    return asyncio.run(_ingest(source_id, url))

async def _ingest(source_id: int, url: str):
    await init_db()
    async with AsyncSessionLocal() as session:
        src = await session.get(Source, source_id)
        src.status = "in_progress"
        await session.commit()

    try:
        docs = load_and_chunk_url(url)

        embed = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=EMBED_MODEL)
        vectordb = Chroma.from_documents(docs, embed, persist_directory=CHROMA_DIR)
        vectordb.persist()

        async with AsyncSessionLocal() as session:
            src = await session.get(Source, source_id)
            src.status = "completed"
            await session.commit()
    except Exception as e:
        async with AsyncSessionLocal() as session:
            src = await session.get(Source, source_id)
            src.status = "failed"
            src.error = str(e)
            await session.commit()
        raise
