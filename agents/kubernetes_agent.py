KUBERNETES_SYSTEM_PROMPT = """
You are a senior Kubernetes and cloud-native infrastructure specialist with 10+ years of experience.

You excel at diagnosing:
- Pod lifecycle issues (CrashLoopBackOff, Pending, Evicted, OOMKilled)
- Service and networking problems (DNS, Ingress, ClusterIP)
- Resource constraints (CPU throttling, memory limits, node pressure)
- RBAC and permission errors
- Deployment rollout failures
- ConfigMap and Secret misconfigurations

When analyzing a Kubernetes issue, always consider:
1. Pod events (kubectl describe pod output)
2. Container logs (kubectl logs)
3. Resource quotas and limits
4. Node health and capacity
5. Network policies

Provide specific kubectl commands in your suggested fixes.
"""


def get_kubernetes_prompt_addition(log_input: str) -> str:
    """Return K8s-specific context hints based on log content."""
    hints = []
    log_lower = log_input.lower()

    if "crashloopbackoff" in log_lower:
        hints.append("HINT: CrashLoopBackOff — check: exit code, resource limits, env vars, application startup errors")
    if "oomkilled" in log_lower or "137" in log_input:
        hints.append("HINT: OOMKilled (exit 137) — memory limit exceeded. Check requests/limits in pod spec")
    if "imagepullbackoff" in log_lower:
        hints.append("HINT: ImagePullBackOff — check: image name/tag, imagePullSecrets, registry access")
    if "pending" in log_lower:
        hints.append("HINT: Pending pod — check: node resources, node selectors, taints/tolerations, PVC binding")
    if "evicted" in log_lower:
        hints.append("HINT: Evicted pod — node was under resource pressure. Check node conditions")

    return "\n".join(hints) if hints else ""