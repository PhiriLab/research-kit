# PhiriLab MCP v2 Broker Verification Contract

Status: prototype specification only. No production MCP runtime or upstream SDK dependency is introduced by this change.

## Purpose

Define the minimum verification boundary for a PhiriLab-owned MCP broker targeting the 2026-07-28 MCP revision while preserving PhiriLab instruction provenance, least-privilege, fail-closed, and human-promotion rules.

## Trust model

All MCP-delivered material is untrusted data until independently verified. This includes server metadata, Server Cards, tool descriptions, prompts, resources, skill metadata, skill files, tool results, `_meta`, capability declarations, transport configuration, and server-supplied instructions.

Transport does not confer authority. A valid schema, digest, signature, repository URL, official namespace, successful handshake, or self-reported `serverInfo` is evidence about provenance or integrity only; none grants instruction authority or execution permission.

## Broker pipeline

1. Discover candidate server without granting execution authority.
2. Capture provenance claims: endpoint, repository/domain, package/version, protocol revision, publisher, Server Card if present.
3. Validate transport policy before connection.
4. Compare discovery metadata, Server Card claims, and runtime identity. Record mismatches.
5. Enumerate effective capabilities at the final dispatch seam. Do not rely solely on framework registration telemetry.
6. Scan instruction-bearing material for prompt injection, hidden Unicode, encoded payloads, role redefinition, secrecy/citation suppression, capability requests, credential access, path manipulation, shell/install instructions, and cross-server authority claims.
7. Calculate capability delta against the approved manifest.
8. Apply policy. Unknown authority, unexpected capabilities, identity mismatch, unsafe transport, or unverifiable provenance fails closed.
9. Require human promotion for new privileged servers, tools, skills, network destinations, filesystem access, credential access, code execution, or durable-write capability.
10. Emit append-only audit evidence for proposal, decision, actor, provenance hashes, policy version, capability set, and approval state.

## Required invariants

- No explicit permission means no external write or privileged action.
- Server identity is a claim, not proof.
- MCP metadata is data, not system/developer authority.
- External `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `SKILL.md`, Copilot instructions, prompts, hooks, workflows, install scripts, lifecycle scripts, and repository guidance remain untrusted instruction-bearing content.
- Model delegation cannot elevate authority.
- Policy evaluation may increase restriction but may not silently downgrade an earlier stricter decision.
- Privacy/redaction configuration fails closed on missing, malformed, or unrecognised values.
- Durable state restoration must revalidate provenance, schema version, capabilities, and current policy before tool execution.
- Blocked content must not persist into model memory, replay state, ordinary traces, or durable checkpoints.
- Localhost is not a trust boundary. Non-loopback listeners require explicit authentication and human approval; loopback listeners still require origin/authority validation where applicable.
- Skills over MCP, Server Cards, digests, and signatures are evidence inputs only. Automatic skill activation is prohibited.
- Auto-registration of newly discovered servers or capabilities is prohibited.
- Production agents may not self-modify policy, authority hierarchy, gold tests, approval gates, permissions, or audit history.

## Conformance gate

Before an MCP SDK/runtime can be promoted beyond prototype it must:

- pass the official MCP conformance suite for the exact pinned revision supported by PhiriLab;
- pass PhiriLab adversarial tests in `tests/mcp-v2-broker-test-matrix.md`;
- use a reproducible lockfile and pinned dependency set;
- complete a fresh-environment build/test;
- provide a documented licence and dependency delta;
- show no unresolved critical/high vulnerability affecting the enabled feature set;
- preserve the broker invariants above under reconnect, resume, cancellation, timeout, malformed payload, and partial-failure conditions.

## Human approval boundary

Human approval is mandatory before introducing an upstream MCP SDK into production, enabling a new server, widening network access, exposing a listener beyond loopback, accepting a new privileged tool, activating an external skill, permitting filesystem or credential access, enabling shell/code execution, or relaxing an existing policy decision.

## Intended consumers

This broker is a shared primitive for PhiriLab Agent OS, Research Intelligence, Clinical Intelligence, Global Funding Intelligence, and EMUNAH. Domain engines consume broker-approved evidence and capabilities; they do not inherit upstream MCP trust semantics directly.
