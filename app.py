import streamlit as st
from utils.helpers import analyze_log_with_rag
from agents.graph import run_agent_pipeline      

st.set_page_config(
    page_title="AI DevOps Assistant",
    page_icon="🚀",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1 style="margin:0;">🚀 AI DevOps Incident Assistant</h1>
    <p style="margin-top:0.5rem;">
        Powered by Ollama + LangChain + RAG
    </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("## ⚙️ Settings")

    model_choice = st.selectbox(
        "🤖 AI Model",
        ["llama3", "mistral", "deepseek-coder"],
        key="model_select"
    )

    issue_type = st.selectbox(
        "🏷️ Issue Type",
        [
            "Auto-Detect",
            "Kubernetes",
            "Docker",
            "CI/CD",
            "Server Error",
            "GitHub Actions"
        ],
        key="issue_select"
    )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "📂 Upload Log File",
        type=["log", "txt"],
        key="file_upload"
    )

    st.markdown("---")
    st.markdown("### 💡 Sample Errors")

    samples = {
        "K8s CrashLoopBackOff":
            "Error: Back-off restarting failed container\n"
            "Kubernetes pod my-app-xyz is in CrashLoopBackOff state",

        "Docker OOM Kill":
            "docker: Error response from daemon: OOMKilled\n"
            "Container exceeded memory limit",

        "GitHub Actions Fail":
            "Run npm test\nERROR: jest is not recognized"
    }

    for idx, (label, text) in enumerate(samples.items()):

        if st.button(
            label,
            use_container_width=True,
            key=f"sample_btn_{idx}"
        ):
            st.session_state["sample_input"] = text

# ── Main Layout ─────────────────────────────────────────────
col_input, col_output = st.columns(2)

# ── Input Column ─────────────────────────────────────────────
# ─────────────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────────────

# INPUT SECTION
st.markdown("## 📋 Incident Input")

default_text = st.session_state.get("sample_input", "")

log_input = st.text_area(
    "Paste your logs or error message",
    value=default_text,
    height=350,
    placeholder="Paste Kubernetes, Docker, CI/CD or server logs here...",
    key="log_input"
)

# FILE PREVIEW
if uploaded_file is not None:

    file_text = uploaded_file.read().decode("utf-8")

    st.markdown("### 📄 Uploaded File Preview")

    st.code(file_text[:500], language="text")

    if not log_input.strip():
        log_input = file_text

# ANALYZE BUTTON
analyze_btn = st.button(
    "🔍 Analyze Incident",
    type="primary",
    use_container_width=True,
    key="analyze_btn"
)

# ─────────────────────────────────────────────────────
# AI ANALYSIS SECTION
# ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 🧠 AI Analysis")

if analyze_btn:
    if not log_input.strip():
        st.warning("⚠️ Please paste an error or upload a log file first.")
    else:
        with st.spinner("🤖 Multi-agent pipeline running..."):
            progress_steps = [
                "🔀 Router agent: detecting issue type...",
                "🔬 Specialist agent: extracting domain hints...",
                "📚 Retrieval agent: searching knowledge base...",
                "🧠 Remediation agent: generating analysis...",
                "📋 Report agent: formatting output...",
            ]
            progress_bar = st.progress(0)
            status_text  = st.empty()

            try:
                for i, step in enumerate(progress_steps):
                    status_text.caption(step)
                    progress_bar.progress((i + 1) * 18)

                result = run_agent_pipeline(
                    log_input=log_input,
                    user_issue_type=issue_type,
                    model_name=model_choice
                )

                progress_bar.progress(100)
                status_text.caption("✅ Pipeline complete!")

                st.session_state["last_result"] = {
                    "analysis":      result.get("analysis", ""),
                    "report":        result.get("final_report", ""),
                    "sources":       result.get("rag_sources", []),
                    "detected_type": result.get("detected_issue_type", ""),
                    "agent_used":    result.get("agent_name", ""),
                    "error":         result.get("error"),
                }

                # Auto-save to SQLite history
                try:
                    detected_severity = "Medium"
                    for lvl in ["Critical", "High", "Medium", "Low"]:
                        if lvl in result.get("analysis", ""):
                            detected_severity = lvl
                            break

                    save_incident(
                        issue_type = result.get("detected_issue_type", "Unknown"),
                        agent_used = result.get("agent_name", "Unknown"),
                        severity   = detected_severity,
                        log_input  = log_input,
                        analysis   = result.get("analysis", ""),
                        sources    = result.get("rag_sources", [])
                    )
                except Exception as save_err:
                    st.caption(f"Note: Could not save to history — {save_err}")

            except Exception as e:
                st.error(f"❌ Pipeline error: {e}")
                st.info("Make sure Ollama is running using:\n`ollama serve`")
# ─────────────────────────────────────────────────────
# RESULT DISPLAY
# ─────────────────────────────────────────────────────
if "last_result" in st.session_state:

    result_data = st.session_state["last_result"]

    if result_data.get("error"):

        st.error(result_data["error"])

    else:

        agent_labels = {
            "kubernetes_agent": "☸️ Kubernetes Specialist",
            "docker_agent": "🐳 Docker Specialist",
            "cicd_agent": "⚙️ CI/CD Specialist",
            "log_agent": "📋 Log Analysis Agent",
        }

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Agent Used",
                agent_labels.get(
                    result_data.get("agent_used", ""),
                    "🤖 AI Agent"
                )
            )

        with metric_col2:
            st.metric(
                "Detected Type",
                result_data.get("detected_type", "Unknown")
            )

        st.markdown("---")

        st.markdown(result_data.get("analysis", ""))

        # KNOWLEDGE SOURCES
        sources = result_data.get("sources", [])

        if sources:

            st.markdown("---")
            st.markdown("### 📚 Knowledge Sources")

            for idx, src in enumerate(sources, 1):

                with st.expander(
                    f"Source {idx} — "
                    f"{src['category']} "
                    f"(score: {src['score']})"
                ):

                    st.code(src["content"], language="text")

                    st.caption(f"📁 {src['source']}")

        # ACTION BUTTONS
        st.markdown("---")

        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:

            st.download_button(
                label="⬇️ Download Report",
                data=result_data.get(
                    "report",
                    result_data.get("analysis", "")
                ),
                file_name="incident_report.md",
                mime="text/markdown",
                use_container_width=True,
                key="download_report_btn"
            )

        with btn_col2:

            if st.button(
                "🔄 Clear Results",
                use_container_width=True,
                key="clear_results_btn"
            ):

                del st.session_state["last_result"]

                st.rerun()
st.markdown("---")

st.caption(
    "🚀 Local AI DevOps Assistant | "
    "Ollama + LangChain + ChromaDB"
)

