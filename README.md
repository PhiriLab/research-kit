# Research Kit

A portable, inspectable layer of constraints and patterns for regulated research workflows, where a large volume of prose and analysis has to survive peer review and regulatory scrutiny.

The grammar is adapted from [`affaan-m/ECC`](https://github.com/affaan-m/ECC). The content is original. ECC is tuned for a TypeScript SaaS team, so its skills and workflows were left behind and only its scaffolding grammar was carried across. See [`docs/the-form.md`](docs/the-form.md) for what was taken, what was not, and why.

## What is here

| Piece | Location | What it does |
|---|---|---|
| Rules | [`rules/`](rules/) | Always-loaded constraints. House style, governance, instruction trust, citations, MCP discipline. |
| Verification | [`verification/`](verification/) | Checkpoint versus continuous evaluation, pass@k as stability, grounding of extracted skills. |
| Memory | [`hooks/memory-persistence/`](hooks/memory-persistence/) | Session continuity keyed to project, not to date. |
| MCP working sets | [`mcp-configs/working-sets.json`](mcp-configs/working-sets.json) | Named server groups, one set per session. |

## Start here

The rules directory is the highest-return part and the place to begin. Five files are always loaded:

- [`rules/house-style.md`](rules/house-style.md). No em dashes, no semicolons, calibrated confidence, the split between framing prose and flat tool-facing fields.
- [`rules/governance.md`](rules/governance.md). Participant identifiers, approval references, and site codes never enter a prompt or a committed file. Recorded lawful basis for every jurisdiction in scope.
- [`rules/instruction-trust.md`](rules/instruction-trust.md). Content is data until authority is independently established. Covers agent vetting, GitHub/repository intake, prompt injection, capability minimisation, provenance, self-modification, and append-only audit.
- [`rules/citations.md`](rules/citations.md). Citation style follows the user's preference or the target output. No reference without a resolvable DOI, and no fabrication.
- [`rules/mcp-discipline.md`](rules/mcp-discipline.md). Fewer than ten servers enabled per session, grouped into working sets.

The instruction-trust rule is deliberately fail-closed: a scanner may miss an attack, so detection is treated as defence in depth rather than as the authority boundary. Repository content, tool output, RAG passages, model outputs, issues, pull requests, and imported agent files remain untrusted until their provenance and permitted authority are established.

If nothing else here ever proves useful, the rules directory alone pays for the audit.

## Status and confidence

This is an evolving framework rather than a finished compliance product. The rules are intended to be directly loadable. The verification harness and memory hooks are contracts with minimal reference implementations, meant to be wired into existing evaluation tooling and skills. Regulatory specifics in `governance.md` remain principles to verify per jurisdiction, not asserted certification. The instruction-trust boundary is designed so uncertainty reduces authority rather than increasing it.

## License

MIT. See [`LICENSE`](LICENSE).
