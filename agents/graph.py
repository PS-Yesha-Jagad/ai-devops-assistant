# from typing import TypedDict, Optional
# from langgraph.graph import StateGraph, END

# from agents.router_agent import detect_issue_type, get_agent_for_issue
# from agents.kubernetes_agent import KUBERNETES_SYSTEM_PROMPT, get_kubernetes_prompt_addition
# from agents.docker_agent import DOCKER_SYSTEM_PROMPT, get_docker_prompt_addition
# from agents.cicd_agent import CICD_SYSTEM_PROMPT, get_cicd_prompt_addition
# from agents.log_agent import LOG_SYSTEM_PROMPT, get_log_prompt_addition
# from agents.remediation_agent import REMEDIATION_PROMPT_TEMPLATE
# from agents.report_agent import generate_report
# from rag.retriever import get_relevant_docs, format_context
# from langchain_community.llms import Ollama
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain


# # ── State schema ─────────────────────────────────────────────────────────────
# # NOTE: Do NOT use 'report' as a key — LangGraph reserves it internally.
# class AgentState(TypedDict):
#     log_input:            str
#     user_issue_type:      str
#     model_name:           str
#     detected_issue_type:  str
#     agent_name:           str
#     agent_hints:          str
#     rag_context:          str
#     rag_sources:          list
#     analysis:             str
#     final_report:         str   # <-- was 'report', renamed to avoid conflict
#     error:                Optional[str]


# # ── Node functions ────────────────────────────────────────────────────────────

# def router_node(state: AgentState) -> AgentState:
#     detected = detect_issue_type(
#         state["log_input"],
#         state.get("user_issue_type", "Auto-Detect")
#     )
#     agent = get_agent_for_issue(detected)
#     return {**state, "detected_issue_type": detected, "agent_name": agent}


# def specialist_node(state: AgentState) -> AgentState:
#     log_input = state["log_input"]
#     agent     = state["agent_name"]

#     if agent == "kubernetes_agent":
#         hints = get_kubernetes_prompt_addition(log_input)
#     elif agent == "docker_agent":
#         hints = get_docker_prompt_addition(log_input)
#     elif agent == "cicd_agent":
#         hints = get_cicd_prompt_addition(log_input)
#     else:
#         hints = get_log_prompt_addition(log_input)

#     return {**state, "agent_hints": hints}


# def retrieval_node(state: AgentState) -> AgentState:
#     docs    = get_relevant_docs(state["log_input"], k=3)
#     context = format_context(docs)
#     return {**state, "rag_context": context, "rag_sources": docs}


# def remediation_node(state: AgentState) -> AgentState:
#     try:
#         llm = Ollama(
#             model=state.get("model_name", "llama3"),
#             base_url="http://localhost:11434"
#         )
#         prompt = PromptTemplate(
#             input_variables=[
#                 "issue_type", "agent_name", "agent_hints",
#                 "context", "log_input"
#             ],
#             template=REMEDIATION_PROMPT_TEMPLATE
#         )
#         chain  = LLMChain(llm=llm, prompt=prompt)
#         result = chain.invoke({
#             "issue_type":  state["detected_issue_type"],
#             "agent_name":  state["agent_name"],
#             "agent_hints": state.get("agent_hints", ""),
#             "context":     state.get("rag_context", ""),
#             "log_input":   state["log_input"],
#         })
#         return {**state, "analysis": result["text"], "error": None}
#     except Exception as e:
#         return {**state, "analysis": "", "error": str(e)}


# def formatting_node(state: AgentState) -> AgentState:
#     # Node renamed from 'report_node' to 'formatting_node' — clearer and avoids
#     # any accidental name collision with LangGraph internals.
#     formatted = generate_report(
#         analysis   = state.get("analysis", ""),
#         log_input  = state["log_input"],
#         issue_type = state["detected_issue_type"],
#         sources    = state.get("rag_sources", [])
#     )
#     return {**state, "final_report": formatted}


# # ── Build the graph ───────────────────────────────────────────────────────────

# def build_agent_graph():
#     graph = StateGraph(AgentState)

#     graph.add_node("router",      router_node)
#     graph.add_node("specialist",  specialist_node)
#     graph.add_node("retrieval",   retrieval_node)
#     graph.add_node("remediation", remediation_node)
#     graph.add_node("formatting",  formatting_node)   # <-- renamed node

#     graph.set_entry_point("router")
#     graph.add_edge("router",      "specialist")
#     graph.add_edge("specialist",  "retrieval")
#     graph.add_edge("retrieval",   "remediation")
#     graph.add_edge("remediation", "formatting")
#     graph.add_edge("formatting",  END)

#     return graph.compile()


# # ── Public entry point ────────────────────────────────────────────────────────

# def run_agent_pipeline(log_input: str,
#                        user_issue_type: str = "Auto-Detect",
#                        model_name: str = "llama3") -> dict:
#     graph = build_agent_graph()

#     initial_state: AgentState = {
#         "log_input":           log_input,
#         "user_issue_type":     user_issue_type,
#         "model_name":          model_name,
#         "detected_issue_type": "",
#         "agent_name":          "",
#         "agent_hints":         "",
#         "rag_context":         "",
#         "rag_sources":         [],
#         "analysis":            "",
#         "final_report":        "",   # <-- was 'report'
#         "error":               None,
#     }

#     final_state = graph.invoke(initial_state)
#     return final_state



from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents.router_agent import detect_issue_type, get_agent_for_issue
from agents.kubernetes_agent import (
    KUBERNETES_SYSTEM_PROMPT,
    get_kubernetes_prompt_addition
)
from agents.docker_agent import (
    DOCKER_SYSTEM_PROMPT,
    get_docker_prompt_addition
)
from agents.cicd_agent import (
    CICD_SYSTEM_PROMPT,
    get_cicd_prompt_addition
)
from agents.log_agent import (
    LOG_SYSTEM_PROMPT,
    get_log_prompt_addition
)

from agents.remediation_agent import REMEDIATION_PROMPT_TEMPLATE
from agents.report_agent import generate_report

from rag.retriever import get_relevant_docs, format_context

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate


# ── State schema ─────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    log_input: str
    user_issue_type: str
    model_name: str

    detected_issue_type: str
    agent_name: str
    agent_hints: str

    rag_context: str
    rag_sources: list

    analysis: str
    final_report: str

    error: Optional[str]


# ── Router Node ──────────────────────────────────────────────────────────────

def router_node(state: AgentState) -> AgentState:

    detected = detect_issue_type(
        state["log_input"],
        state.get("user_issue_type", "Auto-Detect")
    )

    agent = get_agent_for_issue(detected)

    return {
        **state,
        "detected_issue_type": detected,
        "agent_name": agent
    }


# ── Specialist Node ──────────────────────────────────────────────────────────

def specialist_node(state: AgentState) -> AgentState:

    log_input = state["log_input"]
    agent = state["agent_name"]

    if agent == "kubernetes_agent":
        hints = get_kubernetes_prompt_addition(log_input)

    elif agent == "docker_agent":
        hints = get_docker_prompt_addition(log_input)

    elif agent == "cicd_agent":
        hints = get_cicd_prompt_addition(log_input)

    else:
        hints = get_log_prompt_addition(log_input)

    return {
        **state,
        "agent_hints": hints
    }


# ── Retrieval Node ───────────────────────────────────────────────────────────

def retrieval_node(state: AgentState) -> AgentState:

    docs = get_relevant_docs(
        state["log_input"],
        k=3
    )

    context = format_context(docs)

    return {
        **state,
        "rag_context": context,
        "rag_sources": docs
    }


# ── Remediation Node ─────────────────────────────────────────────────────────

def remediation_node(state: AgentState) -> AgentState:

    try:
        llm = Ollama(
            model=state.get("model_name", "llama3"),
            base_url="http://localhost:11434"
        )

        prompt = PromptTemplate(
            input_variables=[
                "issue_type",
                "agent_name",
                "agent_hints",
                "context",
                "log_input"
            ],
            template=REMEDIATION_PROMPT_TEMPLATE
        )

        # NEW LangChain syntax (No LLMChain)
        chain = prompt | llm

        result = chain.invoke({
            "issue_type": state["detected_issue_type"],
            "agent_name": state["agent_name"],
            "agent_hints": state.get("agent_hints", ""),
            "context": state.get("rag_context", ""),
            "log_input": state["log_input"],
        })

        return {
            **state,
            "analysis": result,
            "error": None
        }

    except Exception as e:

        return {
            **state,
            "analysis": "",
            "error": str(e)
        }


# ── Formatting Node ──────────────────────────────────────────────────────────

def formatting_node(state: AgentState) -> AgentState:

    formatted = generate_report(
        analysis=state.get("analysis", ""),
        log_input=state["log_input"],
        issue_type=state["detected_issue_type"],
        sources=state.get("rag_sources", [])
    )

    return {
        **state,
        "final_report": formatted
    }


# ── Build Graph ──────────────────────────────────────────────────────────────

def build_agent_graph():

    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("specialist", specialist_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("remediation", remediation_node)
    graph.add_node("formatting", formatting_node)

    graph.set_entry_point("router")

    graph.add_edge("router", "specialist")
    graph.add_edge("specialist", "retrieval")
    graph.add_edge("retrieval", "remediation")
    graph.add_edge("remediation", "formatting")
    graph.add_edge("formatting", END)

    return graph.compile()


# ── Public Pipeline Entry ────────────────────────────────────────────────────

def run_agent_pipeline(
    log_input: str,
    user_issue_type: str = "Auto-Detect",
    model_name: str = "llama3"
) -> dict:

    graph = build_agent_graph()

    initial_state: AgentState = {
        "log_input": log_input,
        "user_issue_type": user_issue_type,
        "model_name": model_name,

        "detected_issue_type": "",
        "agent_name": "",
        "agent_hints": "",

        "rag_context": "",
        "rag_sources": [],

        "analysis": "",
        "final_report": "",

        "error": None,
    }

    final_state = graph.invoke(initial_state)

    return final_state