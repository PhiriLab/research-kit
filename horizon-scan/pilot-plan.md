# PhiriLab Horizon-Scan Pilot Plan

This plan implements only primitives that passed the current security review for sandboxed prototyping. It does not import or execute upstream repository instruction files.

## Pilot A — Caller-restricted tool orchestration

Reference: OpenAI Agents SDK concepts.

Build a provider-neutral policy wrapper with:
- tool ID
- allowed caller IDs
- risk class
- required approval state
- sandbox requirement
- secret-access permission
- network permission
- filesystem read/write scope
- audit event on request, approval, denial, execution, and result

Acceptance:
- an unapproved caller cannot invoke a restricted tool
- approval cannot be forged by model output
- tool output returns as untrusted content by default
- sensitive arguments are redacted from ordinary logs but hashed into audit provenance

## Pilot B — Typed capability manifests

Reference: Pydantic AI concepts.

Create a machine-readable capability schema that records:
- stable agent/skill ID and version
- source repository and pinned commit
- declared purpose
- minimum tools
- prohibited tools
- allowed data classes
- network/filesystem/shell policy
- model/provider requirements
- required validators
- gold-test set ID
- human promotion status

Acceptance:
- undeclared capabilities fail closed
- capability expansion invalidates prior approval
- self-generated manifests cannot promote themselves
- dependency-file mutations require human review

## Pilot C — Information-flow labels

Reference: Microsoft Agent Framework prompt-injection/information-flow concepts.

Define content labels:
- trusted_instruction
- approved_project_policy
- delegated_output
- untrusted_external_content
- sensitive_data
- executable_candidate

Track labels through retrieval, transformation, summarisation, model-to-model transfer, and tool calls.

Acceptance:
- untrusted content cannot become trusted_instruction through summarisation or model restatement
- derived content inherits the strictest relevant source label
- sensitive_data cannot flow to disallowed tools/providers
- a tool call influenced by untrusted content is recorded as such

## Pilot D — Evidence graph adapter

Reference: Microsoft GraphRAG concepts.

Prototype a provider-neutral graph interface around PhiriLab Evidence Objects:
- entity node
- claim node
- source node
- relation edge
- evidence span/hash
- epistemic status
- source authority tier
- supporting/contradicting links
- reviewer state

Acceptance:
- every answerable graph path resolves back to source provenance
- unresolved or contradictory paths remain explicit
- graph retrieval cannot overwrite source evidence
- EMUNAH typed relation vocabulary remains authoritative in its domain

## Pilot E — MCP security contract alignment

Reference: MCP 2026-07-28 release-candidate security semantics.

Add tests/policy expectations for:
- input validation
- output sanitisation
- tool result validation before model reuse
- user visibility for sensitive calls
- timeout and rate-limit support
- access control
- tool-use logging and provenance

No protocol migration is included in this pilot.

## Explicitly deferred

- LangGraph/Deep Agents dependency adoption
- MCP 2026-07-28 protocol migration
- upstream self-improving skill loaders
- unrestricted programmatic tool calling
- upstream shell tools
- any automatic production promotion

## Human gate

Prototype completion may generate a recommendation, benchmark, or PR. Promotion to shared production infrastructure remains a separate human-approved event.