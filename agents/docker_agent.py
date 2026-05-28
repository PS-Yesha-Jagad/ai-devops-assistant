DOCKER_SYSTEM_PROMPT = """
You are a Docker and container infrastructure expert with deep knowledge of containerization best practices.

You excel at diagnosing:
- Container startup failures and exit codes
- Image build errors and layer caching issues
- Networking problems (port conflicts, bridge networks, DNS)
- Volume mount and permission errors
- Docker Compose service dependencies
- Registry authentication failures
- Resource constraints (OOM, CPU limits)

When analyzing a Docker issue, always consider:
1. Container exit codes (0=clean, 1=error, 137=OOM, 139=segfault)
2. Docker daemon logs
3. Image layers and Dockerfile instructions
4. Network configuration
5. Volume permissions

Provide specific docker commands in your suggested fixes.
"""


def get_docker_prompt_addition(log_input: str) -> str:
    """Return Docker-specific context hints based on log content."""
    hints = []
    log_lower = log_input.lower()

    if "oom" in log_lower or "memory" in log_lower:
        hints.append("HINT: Memory issue — check docker stats, increase --memory flag, or fix memory leak")
    if "port" in log_lower and ("bind" in log_lower or "use" in log_lower):
        hints.append("HINT: Port conflict — run: docker ps to find the conflicting container")
    if "permission" in log_lower or "denied" in log_lower:
        hints.append("HINT: Permission error — check volume ownership and USER instruction in Dockerfile")
    if "pull" in log_lower or "unauthorized" in log_lower:
        hints.append("HINT: Registry auth — run: docker login before pulling")

    return "\n".join(hints) if hints else ""