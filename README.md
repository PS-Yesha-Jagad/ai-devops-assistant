# 🚀 AI DevOps Incident Resolution Assistant

> An AI-powered DevOps troubleshooting assistant that analyzes Kubernetes,
> Docker, and CI/CD logs using local LLMs, RAG, and a multi-agent system.
> Runs 100% locally — no API keys, no cloud cost.


---

## What It Does

Paste a Kubernetes, Docker, or CI/CD error and get back:

- **Root cause analysis** — what went wrong and why
- **Severity rating** — Critical / High / Medium / Low
- **Step-by-step fix** — exact commands to run
- **Knowledge retrieval** — relevant docs pulled from a local vector database

---

## Architecture

```
User Input (log / error)
        ↓
  Streamlit UI
        ↓
 LangGraph Router
        ↓
┌──────────────────────────────┐
│  Specialist Agents           │
│  ☸️  Kubernetes Agent        │
│  🐳  Docker Agent            │
│  ⚙️  CI/CD Agent             │
│  📋  Log Analysis Agent      │
└──────────────────────────────┘
        ↓
  RAG Retrieval (ChromaDB)
        ↓
  Ollama LLM (Llama3 / Mistral)
        ↓
  Structured Incident Report
```

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| UI          | Streamlit                         |
| Agents      | LangGraph state machine           |
| RAG         | LangChain + ChromaDB              |
| LLM         | Ollama (Llama3, Mistral)          |
| Embeddings  | nomic-embed-text via Ollama       |
| Language    | Python 3.11                       |

---

## Local Setup

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/download) installed

### Install

```bash
git clone https://github.com/YOUR_USERNAME/ai-devops-assistant.git
cd ai-devops-assistant
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
python setup.py
```

### Run

```bash
# Terminal 1 — keep Ollama running
ollama serve

# Terminal 2 — start the app
streamlit run app.py
```

Open `http://localhost:8501`

---

## Sample Errors to Try

**Kubernetes:**
```
pod/api-service-7d9f8 CrashLoopBackOff
Exit Code: 137 - OOMKilled
Memory limit 256Mi exceeded
```

**Docker:**
```
docker: Error response from daemon: driver failed programming
external connectivity: Bind for 0.0.0.0:8080 failed: port is already allocated
```

**GitHub Actions:**
```
Run npm test
jest: command not found
Error: Process completed with exit code 127
```

---

## Project Structure

```
ai-devops-assistant/
├── app.py                    # Streamlit UI
├── agents/
│   ├── graph.py              # LangGraph orchestrator
│   ├── router_agent.py       # Issue type detector
│   ├── kubernetes_agent.py   # K8s specialist
│   ├── docker_agent.py       # Docker specialist
│   ├── cicd_agent.py         # CI/CD specialist
│   ├── log_agent.py          # General log analyst
│   ├── remediation_agent.py  # Fix suggestion prompt
│   └── report_agent.py       # Report formatter
├── rag/
│   ├── ingest.py             # One-time KB loader
│   ├── retriever.py          # Query-time search
│   ├── chunking.py           # Text splitter
│   ├── embeddings.py         # Ollama embeddings
│   └── vectorstore.py        # ChromaDB wrapper
├── knowledge_base/
│   ├── kubernetes_docs/
│   ├── docker_docs/
│   └── cicd_docs/
├── utils/
│   ├── helpers.py            # LLM chain builder
│   ├── memory.py             # SQLite history
│   └── logger.py
└── setup.py                  # One-command setup
```

---

## Skills Demonstrated

| Skill | Implementation |
|---|---|
| Generative AI | Ollama + Llama3 local LLM |
| RAG | LangChain + ChromaDB semantic search |
| Multi-agent systems | LangGraph state machine |
| Vector databases | ChromaDB with nomic embeddings |
| Local LLMs | Ollama inference server |
| Python | Full-stack backend |
| UI development | Streamlit dashboard |
