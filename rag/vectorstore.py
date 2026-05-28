from langchain_community.vectorstores import Chroma
from rag.embeddings import get_embeddings
import os

CHROMA_PATH = "./chroma_db"


def get_vectorstore():
    """Load existing ChromaDB or return None if not yet created."""
    embeddings = get_embeddings()
    if os.path.exists(CHROMA_PATH):
        return Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
    return None


def create_vectorstore(chunks: list):
    """Create a new ChromaDB from document chunks."""
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    vectorstore.persist()
    print(f"ChromaDB created and saved to {CHROMA_PATH}")
    return vectorstore