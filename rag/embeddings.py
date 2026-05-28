from langchain_community.embeddings import OllamaEmbeddings


def get_embeddings(model_name: str = "nomic-embed-text"):
    """Return an Ollama embedding model instance."""
    return OllamaEmbeddings(
        model=model_name,
        base_url="http://localhost:11434"
    )
