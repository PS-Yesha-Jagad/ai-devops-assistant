LOG_SYSTEM_PROMPT = """
You are a general-purpose systems reliability engineer (SRE) and log analysis expert.

You excel at diagnosing:
- Application errors and stack traces
- Server-side errors (HTTP 500, 502, 503, 504)
- Database connection and query failures
- Memory leaks and performance degradation
- Authentication and authorization errors
- Configuration file problems
- Dependency and version conflicts

When analyzing a general log or error:
1. Identify the error type and component
2. Look for patterns (repeated errors, cascading failures)
3. Check timestamps for correlation
4. Identify the root component vs downstream effects
5. Suggest both immediate fixes and long-term improvements
"""


def get_log_prompt_addition(log_input: str) -> str:
    """Return general log analysis hints."""
    hints = []
    log_lower = log_input.lower()

    if "connection refused" in log_lower:
        hints.append("HINT: Connection refused — target service may be down or wrong host/port configured")
    if "timeout" in log_lower:
        hints.append("HINT: Timeout — check network connectivity, service health, and timeout configuration")
    if "null" in log_lower or "nullpointer" in log_lower:
        hints.append("HINT: Null pointer — uninitialized variable or missing configuration value")
    if "disk" in log_lower or "no space" in log_lower:
        hints.append("HINT: Disk space issue — run: df -h to check disk usage")

    return "\n".join(hints) if hints else ""