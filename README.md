# Research Kit

A portable, inspectable layer of constraints and patterns for regulated research workflows, where a large volume of prose and analysis has to survive peer review and regulatory scrutiny.

The grammar is adapted from [`affaan-m/ECC`](https://github.com/affaan-m/ECC). The content is original. ECC is tuned for a TypeScript SaaS team, so its skills and workflows were left behind and only its scaffolding grammar was carried across. See [`docs/the-form.md`](docs/the-form.md) for what was taken, what was not, and why.

## What is here

| Piece | Location | What it does |
|---|---|---|
| Rules | [`rules/`](rules/) | Always-loaded constraints. House style, governance, citations, MCP discipline, provenance hygiene. |
| Verification | [`verification/`](verification/) | Checkpoint versus continuous evaluation, pass@k as stability, grounding of extracted skills. |
| Memory | [`hooks/memory-persistence/`](hooks/memory-persistence/) | Session continuity keyed to project, not to date. |
| MCP working sets | [`mcp-configs/working-sets.json`](mcp-configs/working-sets.json) | Named server groups, one set per session. |
| Provenance hygiene | [`skills/provenance-content-hygiene/`](skills/provenance-content-hygiene/) | Cross-model authorial-integrity policy plus conservative hidden-Unicode and metadata inspection. |

## Start here

The rules directory is the highest-return part and the place to begin. Five files, always loaded, small and boring by design:

- [`rules/house-style.md`](rules/house-style.md). No em dashes, no semicolons, calibrated confidence, the split between framing prose and flat tool-facing fields.
- [`rules/governance.md`](rules/governance.md). Participant identifiers, approval references, and site codes never enter a prompt or a committed file. Recorded lawful basis for every jurisdiction in scope.
- [`rules/citations.md`](rules/citations.md). Citation style follows the user's preference or the target output. No reference without a resolvable DOI, and no fabrication.
- [`rules/mcp-discipline.md`](rules/mcp-discipline.md). Fewer than ten servers enabled per session, grouped into working sets.
- [`rules/provenance-hygiene.md`](rules/provenance-hygiene.md). Protect user authorship, avoid non-essential hidden markers, preserve multilingual Unicode, and separate authorship from model assistance and file provenance.

## Cross-model provenance hygiene

The provenance component can be installed into Claude Code and Gemini CLI from the same source of truth:

```bash
python3 scripts/install_provenance_hygiene.py --all
```

It also includes a model-independent command-line inspector/cleaner and a ChatGPT instruction profile. See [`docs/provenance-content-hygiene.md`](docs/provenance-content-hygiene.md).

## Status and confidence

This remains a compact framework rather than a full agent operating system. The core rules are ready to load. The provenance hygiene engine is dependency-free and regression-tested, but its file-level metadata scan is deliberately conservative and indicative rather than a forensic parser. Regulatory specifics in `governance.md` are stated as principles to verify per jurisdiction, not as asserted facts.

## License

MIT. See [`LICENSE`](LICENSE).
