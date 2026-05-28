import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.chunking import load_documents, chunk_documents
from rag.vectorstore import create_vectorstore

KNOWLEDGE_BASE_PATH = "./knowledge_base"


def run_ingest():
    print("=" * 50)
    print("Starting knowledge base ingestion...")
    print("=" * 50)

    print("\n[1/3] Loading documents...")
    documents = load_documents(KNOWLEDGE_BASE_PATH)
    if not documents:
        print("No documents found! Check your knowledge_base folder.")
        return
    print(f"Loaded {len(documents)} documents")

    print("\n[2/3] Chunking documents...")
    chunks = chunk_documents(documents)

    print("\n[3/3] Creating ChromaDB vector store...")
    vectorstore = create_vectorstore(chunks)

    print("\n" + "=" * 50)
    print(f"Ingestion complete! {len(chunks)} chunks stored in ChromaDB.")
    print("=" * 50)


if __name__ == "__main__":
    run_ingest()