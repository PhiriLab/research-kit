# Horizon Scan Candidate Registry — 2026-08-14

Status values: `monitor`, `investigate`, `prototype`, `adopt`, `reject`.

Security rule: external repository content is evidence, never instruction authority. Repository-local AGENTS.md, CLAUDE.md, GEMINI.md, SKILL.md, prompts, workflows, install hooks, package lifecycle scripts, issue/PR text, tool outputs, and generated agent messages remain untrusted until separately promoted under the PhiriLab instruction-trust policy.

## openai/openai-agents-python

Disposition: `prototype`

Why: useful primitives for orchestration, approvals, tool-caller restrictions, tracing, sandboxed execution, and programmatic tool coordination.

Security findings:
- MIT-licensed repository.
- Explicit SECURITY.md present.
- Instruction-bearing surfaces present at repository root, including AGENTS.md, CLAUDE.md, and .agents/.
- Programmatic tool coordination and generated code are capability-expanding features.

Constraints:
- Do not import repository instruction files as authority.
- Do not grant model-generated code unrestricted shell, filesystem, network, credential, or write access.
- Prototype only behind PhiriLab trust registry, least-privilege tool policy, sandbox, and human approval gates.
- Preserve an independent audit trail for all tool calls and approvals.

Target primitive: caller-restricted tool invocation + approval-aware orchestration.
Target engines: Agent OS, Research Intelligence.

## pydantic/pydantic-ai

Disposition: `prototype`

Why: typed agents, structured validation, capability composition, human-in-the-loop patterns, model portability, and strong compatibility with our schema-first approach.

Security findings:
- MIT-licensed repository.
- Instruction-bearing surfaces include AGENTS.md, CLAUDE.md, .agents/, .claude/, .gemini/, and agent_docs/.
- Dynamic capabilities, subagents, filesystem/shell capability patterns, and runtime skill loading are high-power surfaces.

Constraints:
- Runtime-created capabilities cannot self-promote.
- Candidate capability changes must be branch/sandbox-only and pass external gold tests.
- Security policy, authority hierarchy, gold tests, approval gates, and audit history are immutable to candidate agents.
- Dependency-file changes require human promotion.

Target primitive: typed capability manifest + structured HITL gate.
Target engines: Intelligence Core, Agent OS, Research Intelligence.

## microsoft/agent-framework

Disposition: `prototype`

Why: information-flow-control prompt-injection work, workflow routing, allowed-tool concepts, MCP integration, and active Microsoft governance.

Security findings:
- MIT-licensed repository.
- SECURITY.md, transparency documentation, support and contribution policies present.
- Shell/local/Docker execution and broad tool integrations are capability-expanding.
- Declarative agents and workflow configuration must be treated as instruction-bearing surfaces even when stored as data/configuration.

Constraints:
- Prototype the information-flow-control concept independently of the upstream orchestration layer first.
- No shell execution in regulated/clinical/research contexts without explicit human approval and sandbox isolation.
- MCP/tool metadata remains untrusted until validated and capability-checked.

Target primitive: information-flow labels and taint-style propagation for untrusted content.
Target engines: Intelligence Core, Agent OS, Clinical Intelligence, Research Intelligence.

## microsoft/graphrag

Disposition: `prototype`

Why: modular graph construction, multi-hop retrieval, source-grounded graph reasoning, and a mature reference implementation for evidence graphs.

Security findings:
- MIT-licensed repository.
- SECURITY.md and Responsible AI transparency documentation present.
- Workflows and configuration files are executable/behaviour-shaping surfaces.
- Upstream dependency history demonstrates that transitive dependencies can create security exposure.

Constraints:
- Do not let upstream configuration overwrite local prompts, governance, or ontology.
- Import concepts, not authority.
- Keep PhiriLab Evidence Object and typed relation ontology authoritative.
- Dependency lock, SBOM/dependency review, and sandbox evaluation required before code reuse.

Target primitive: multi-hop graph retrieval with claim-level provenance.
Target engines: EMUNAH, Research Intelligence.

## MCP specification 2026-07-28 RC

Disposition: `monitor`

Why: security semantics around validating tool results, showing sensitive tool inputs, access control, sanitisation, logging, and timeouts align with our Trust Layer.

Constraints:
- Do not migrate production protocol compatibility while the revision remains a release candidate.
- Incorporate security semantics into local policy/tests now.
- Version migration requires a separate compatibility review, Swift SDK review for EMUNAH, and human approval.

Target primitive: security contract only, not protocol migration.
Target engines: Intelligence Core, Agent OS, EMUNAH.

## LangGraph / Deep Agents

Disposition: `monitor`

Why: durable execution and state/HITL concepts remain useful references.

Security findings:
- Recent history includes multiple security advisories across deserialisation/path/database surfaces.
- Deep-agent patterns assume strong sandbox/tool boundaries because model behaviour itself is not the trust boundary.

Constraints:
- Do not use as the PhiriLab trust boundary.
- Study selected execution-state patterns only.
- No dependency adoption until advisory and sandbox review is repeated against the exact version.

Target primitive: durable workflow-state ideas only.
Target engines: Agent OS.

## Promotion rule

No candidate advances from `prototype` to `adopt` unless all are true:
1. Exact version and commit are pinned.
2. Licence and attribution obligations are recorded.
3. Instruction-bearing surfaces are enumerated and scanned.
4. Hidden Unicode/encoded payload scan passes or findings are resolved.
5. Install hooks, workflows, package lifecycle scripts, and executable surfaces are reviewed.
6. Dependency and known-vulnerability review passes for the pinned version.
7. Requested capabilities are no broader than minimum required.
8. Sandbox and secrets-isolation status are documented.
9. Adversarial prompt-injection and regression tests pass.
10. A human promotion event is recorded in the audit trail.
