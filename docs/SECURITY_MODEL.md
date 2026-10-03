# Security Model

Trust boundaries: user/client, control plane, model providers, MCP servers, A2A agents, enterprise connectors, artifact storage and memory.

Core controls: OIDC/workload identity, trusted tenant claims, RBAC/ABAC, policy-as-code, least-privilege short-lived credentials, KMS/Vault, DLP, egress controls, schema validation, action-hash approvals, idempotency, callback verification, SSRF defense, sandboxing, immutable audit and tenant isolation.

Retrieved content and tool results are untrusted data. An LLM never grants authorization.
