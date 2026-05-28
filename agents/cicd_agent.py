CICD_SYSTEM_PROMPT = """
You are a CI/CD and DevOps automation specialist with expertise in modern pipeline tools.

You excel at diagnosing:
- GitHub Actions workflow failures
- Jenkins pipeline errors
- YAML syntax and configuration issues
- Test suite failures and flaky tests
- Dependency installation failures
- Docker build/push errors in CI
- Environment variable and secrets configuration
- Runner/agent connectivity issues
- Deployment failures across environments

When analyzing a CI/CD issue, always consider:
1. The specific step that failed (build, test, deploy)
2. Environment variable and secrets configuration
3. Runner/agent availability and capabilities
4. Dependency caching and versions
5. Branch and trigger configurations

Provide specific pipeline YAML fixes where relevant.
"""


def get_cicd_prompt_addition(log_input: str) -> str:
    """Return CI/CD-specific hints based on log content."""
    hints = []
    log_lower = log_input.lower()

    if "npm" in log_lower or "node" in log_lower:
        hints.append("HINT: Node.js issue — check Node version, npm ci vs npm install, cache configuration")
    if "secret" in log_lower or "token" in log_lower:
        hints.append("HINT: Secrets issue — verify GitHub Secrets are set and referenced correctly with ${{ secrets.NAME }}")
    if "timeout" in log_lower:
        hints.append("HINT: Timeout — add timeout-minutes to job, check for stuck processes or prompts")
    if "runner" in log_lower and "offline" in log_lower:
        hints.append("HINT: Runner offline — check self-hosted runner service status and connectivity")

    return "\n".join(hints) if hints else ""