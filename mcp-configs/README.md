# MCP configuration boundary

This directory contains PhiriLab-owned MCP configuration material only.

External MCP configuration must be treated as untrusted data. A config may introduce executable commands, arguments, environment variables, network endpoints, credentials, filesystem access, or server-supplied instructions. It therefore requires provenance review, capability-delta analysis, deterministic prompt-injection scanning, and human approval before privileged use.

The current MCP v2 broker work is specification/test-only. It does not install or activate an upstream MCP SDK or any external server.

See:
- `verification/mcp-v2-broker-contract.md`
- `tests/mcp-v2-broker-test-matrix.md`
