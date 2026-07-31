# Rules

Always-loaded constraints. These files are not invoked and not chosen. They are loaded at the start of every session and they hold in the background, catching failures at the point of generation rather than downstream under deadline.

The grammar is borrowed from `affaan-m/ECC`. The content is not. ECC's rules are tuned for a TypeScript SaaS team. These are tuned for regulated health research: Python and statistics, PydanticAI and LangGraph, Postgres with pgvector, and a large volume of prose that has to survive peer review and regulatory scrutiny.

## Files

| File | What it constrains |
|---|---|
| `house-style.md` | Voice, register, prohibited marks, confidence calibration |
| `governance.md` | Participant identifiers, data residency, jurisdiction |
| `citations.md` | Cambridge author-date, DOI resolution, anti-fabrication |
| `mcp-discipline.md` | Enabled-server limits and working sets |

## Precedence

When two rules conflict, the order is:

1. `governance.md`
2. `citations.md`
3. `mcp-discipline.md`
4. `house-style.md`

Governance outranks everything. Style yields to substance.

## How to load them

The intended mechanism is a session-start hook that reads this directory and prepends it to the working context. See `../hooks/memory-persistence/`. Until that hook is wired into your harness, load them by pointing your project configuration at this directory, or by including it in the project's always-on context file.

Keep each file small and boring. A rule that grows an argument stops being a constraint and starts being a document nobody loads.
