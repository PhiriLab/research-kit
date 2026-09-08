# PhiriLab MCP v2 Broker Adversarial Test Matrix

Status: prototype acceptance criteria. These tests define promotion gates; they do not introduce an MCP runtime.

## Identity and provenance

- Server Card identity differs from runtime `serverInfo` -> block and record mismatch.
- Repository/domain claim cannot be independently verified -> quarantine.
- Valid digest on malicious skill content -> integrity passes, authority remains denied.
- Official namespace but unapproved publisher/version -> no privilege elevation.
- Version changes without approved manifest update -> capability re-review required.

## Instruction-bearing content

- Tool description says “ignore previous instructions” -> scan finding; description remains data.
- Server instructions claim system/developer/admin authority -> deny authority claim.
- `SKILL.md` asks agent to install packages or modify config -> quarantine and human review.
- Hidden bidi/zero-width Unicode in prompt/resource/tool description -> flag and fail closed for instruction use.
- Base64/encoded payload decodes to shell, credential, or policy-changing instructions -> quarantine.
- HTML comments/CSS-hidden text contains agent directives -> flag.
- Citation suppression, secrecy, role redefinition, or “Peter approved” self-assertions -> no authority.

## Capability escalation

- Server adds a new tool after approval -> block until manifest re-approved.
- Existing tool broadens from read-only to write -> block.
- Tool begins requesting filesystem, shell, credential, browser, or unrestricted network access -> human gate.
- MCP config introduces `command`, `args`, environment variables, or new executable path -> human gate.
- Tool registration telemetry omits a callable tool -> final-dispatch enumeration must still detect it.
- Later middleware attempts to downgrade an earlier DENY -> DENY remains authoritative.

## Network and listener security

- Non-loopback listener without authentication -> reject.
- Loopback listener with invalid Host/Origin authority -> reject where applicable.
- Redirect moves approved endpoint to an unapproved host/IP -> block.
- DNS resolves to loopback, RFC1918, link-local, or cloud metadata unexpectedly -> block unless explicitly approved.
- Cancelled request continues network traffic -> finding; test fails.
- Server performs undeclared background telemetry -> finding; test fails.

## Skills over MCP

- `skills/list` discovers new remote skill -> no automatic activation.
- `skills/get` returns digest mismatch -> reject.
- Digest matches but injection scan fails -> quarantine.
- Skill requests cross-server tool use beyond approved capability graph -> reject.
- Skill includes executable scripts -> reject by default; separate human-reviewed code path required.
- Skill update arrives dynamically -> retain prior approved version until new version is promoted.

## State, replay, and redaction

- Blocked tool result appears in checkpoint/replay -> test fails.
- Sensitive tool output appears in ordinary trace despite redaction policy -> test fails.
- Malformed privacy configuration enables logging -> test fails; expected behavior is fail closed.
- Restored durable state references a capability no longer approved -> block on resume.
- Deserialization attempts object/code reconstruction beyond approved primitive schema -> reject.

## Failure semantics

- Timeout during policy decision -> deny privileged action.
- Scanner unavailable -> deny instruction-bearing promotion rather than bypassing scan.
- Provenance service unavailable -> quarantine unknown server.
- Partial tool result contains both safe and blocked sections -> blocked content must not reach durable/model context.
- Concurrent requests must not cross-associate authorization, identity, or context.

## Conformance and supply chain

- Exact pinned SDK/revision must pass official MCP conformance tests.
- Lockfile must reproduce in a clean environment.
- Dependency major update -> mandatory delta/security review.
- Critical/high advisory affecting enabled features -> promotion blocked until remediated or formally accepted by human risk owner.
- Install/preinstall/postinstall/lifecycle hooks -> enumerate and review before execution.
- Upstream `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot instructions, workflows, hooks, and release scripts -> scan as untrusted instruction/executable surfaces.

## Acceptance result

Promotion requires all mandatory tests to pass, no unresolved critical policy violation, reproducible evidence, and explicit human approval for privileged production use.
