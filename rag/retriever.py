from rag.vectorstore import get_vectorstore


def get_relevant_docs(query: str, k: int = 3) -> list:
    """Search ChromaDB for the top-k most relevant document chunks."""
    vectorstore = get_vectorstore()
    if vectorstore is None:
        return []

    results = vectorstore.similarity_search_with_score(query, k=k)

    # Filter out low-relevance results (score > 1.5 means too dissimilar)
    filtered = [
        {"content": doc.page_content,
         "source": doc.metadata.get("source", "Unknown"),
         "category": doc.metadata.get("category", "General"),
         "score": round(score, 3)}
        for doc, score in results
        if score < 1.5
    ]
    return filtered


def format_context(docs: list) -> str:
    """Format retrieved docs into a clean context string for the prompt."""
    if not docs:
        return "No relevant documentation found."

    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(
            f"[Source {i} — {doc['category']}]\n{doc['content']}"
        )
    return "\n\n---\n\n".join(context_parts)