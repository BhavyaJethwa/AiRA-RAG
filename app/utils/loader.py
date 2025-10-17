import hashlib
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def load_and_chunk_url(url: str, chunk_size: int = 800, chunk_overlap: int = 200):
    """
    Fetch a URL using LangChain WebBaseLoader, split into chunks,
    and deduplicate chunks via SHA256 hash.
    """
    loader = WebBaseLoader(url)
    docs = loader.load()  # list of Document objects

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = splitter.split_documents(docs)

    # Deduplicate chunks
    seen_hashes = set()
    deduped_docs = []
    for doc in split_docs:
        chunk_hash = hashlib.sha256(doc.page_content.encode("utf-8")).hexdigest()
        if chunk_hash not in seen_hashes:
            deduped_docs.append(doc)
            seen_hashes.add(chunk_hash)

    return deduped_docs
