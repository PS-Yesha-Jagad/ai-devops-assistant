from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from rag.retriever import get_relevant_docs, format_context


def get_llm(model_name: str = "llama3"):
    """Returns Ollama LLM instance.It creates and return ollama instance """
    
    return Ollama(
        model=model_name,
        base_url="http://localhost:11434"
    )


def analyze_log_with_rag(
    log_input: str,
    issue_type: str = "Auto-Detect",
    model_name: str = "llama3"
) -> dict:
    """
    Full RAG pipeline:
    1. Retrieve relevant docs from ChromaDB
    2. Inject them into the prompt as context
    3. Call Ollama LLM with enriched prompt
    Returns both the AI response and retrieved sources.
    """

    # Step 1: Retrieve relevant docs
    relevant_docs = get_relevant_docs(log_input, k=3)

    # Step 2: Format retrieved context
    context = format_context(relevant_docs)

    # Step 3: Load Ollama model
    llm = get_llm(model_name)

    # Step 4: Build RAG prompt
    prompt = PromptTemplate(
        input_variables=[
            "issue_type",
            "log_input",
            "context"
        ],
        template="""
You are an expert DevOps engineer and incident response specialist.

RELEVANT KNOWLEDGE BASE CONTEXT:
{context}

---

A user has submitted the following {issue_type} issue for analysis.

LOG / ERROR:
{log_input}

Using the context above AND your own expertise, respond in EXACTLY this format:

## Issue Type
[Kubernetes / Docker / CI-CD / Server / Unknown]

## Severity
[Critical / High / Medium / Low]

## Root Cause
[2-3 sentences explaining the most likely root cause]

## What is Happening
[Plain English explanation of what the error means]

## Suggested Fix
[3-5 numbered steps to resolve this issue]

## Prevention
[1-2 tips to prevent this issue in future]
"""
    )

    # Modern LangChain runnable chain
    chain = prompt | llm

    # Step 5: Invoke chain
    result = chain.invoke({
        "issue_type": issue_type,
        "log_input": log_input,
        "context": context
    })

    return {
        "analysis": result,
        "sources": relevant_docs
    }


# Backward compatibility function
def analyze_log(
    log_input: str,
    issue_type: str = "Auto-Detect",
    model_name: str = "llama3"
) -> str:

    result = analyze_log_with_rag(
        log_input,
        issue_type,
        model_name
    )

    return result["analysis"]