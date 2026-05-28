from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import os


def load_documents(directory: str) -> list:
    """Load all .txt files from a directory recursively."""
    documents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                try:
                    loader = TextLoader(filepath, encoding="utf-8")
                    docs = loader.load()
                    # Tag each doc with its source category
                    for doc in docs:
                        doc.metadata["source"] = filepath
                        if "kubernetes" in filepath.lower():
                            doc.metadata["category"] = "Kubernetes"
                        elif "docker" in filepath.lower():
                            doc.metadata["category"] = "Docker"
                        elif "cicd" in filepath.lower():
                            doc.metadata["category"] = "CI/CD"
                        else:
                            doc.metadata["category"] = "General"
                    documents.extend(docs)
                except Exception as e:
                    print(f"Warning: Could not load {filepath}: {e}")
    return documents


def chunk_documents(documents: list, chunk_size: int = 500,
                    chunk_overlap: int = 50) -> list:
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks