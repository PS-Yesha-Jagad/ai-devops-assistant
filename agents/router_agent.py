import re

# Keyword maps for routing decisions
ROUTING_RULES = {
    "kubernetes": [
        "crashloopbackoff", "crashloop", "kubernetes", "kubectl", "k8s",
        "pod", "deployment", "ingress", "namespace", "configmap",
        "statefulset", "daemonset", "replicaset", "oomkilled",
        "imagepullbackoff", "pending", "evicted", "node"
    ],
    "docker": [
        "docker", "container", "dockerfile", "image", "registry",
        "docker-compose", "compose", "dockerhub", "entrypoint",
        "volume", "port binding", "network", "daemon"
    ],
    "cicd": [
        "github actions", "jenkins", "pipeline", "ci/cd", "workflow",
        "build failed", "test failed", "deploy", "runner", "artifact",
        "gitlab", "circleci", "travis", "yaml", "yml", ".github"
    ],
}


def detect_issue_type(text: str, user_selected: str = "Auto-Detect") -> str:
    """
    Route the input to the correct agent.
    If user explicitly selected a type, respect it.
    Otherwise, keyword-match the log text.
    """
    if user_selected != "Auto-Detect":
        return user_selected

    text_lower = text.lower()

    scores = {category: 0 for category in ROUTING_RULES}
    for category, keywords in ROUTING_RULES.items():
        for kw in keywords:
            if kw in text_lower:
                scores[category] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "General"
    return best.upper() if best != "cicd" else "CI/CD"


def get_agent_for_issue(issue_type: str) -> str:
    """Return the agent name that should handle this issue type."""
    mapping = {
        "KUBERNETES": "kubernetes_agent",
        "DOCKER":     "docker_agent",
        "CI/CD":      "cicd_agent",
        "General":    "log_agent",
    }
    return mapping.get(issue_type.upper(), "log_agent")