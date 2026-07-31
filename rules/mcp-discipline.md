# MCP Discipline

Always loaded. Every enabled MCP server spends context whether or not it is used. A context window near 200k tokens degrades toward roughly 70k of usable working room when everything is switched on. Confidence 0.7 on the exact numbers, they come from the source framework's rule of thumb, but the direction is not in doubt.

## The rule of thumb

- Configure many servers, twenty to thirty is fine.
- Keep fewer than ten enabled per project.
- Stay under roughly eighty active tools in any one session.
- If a server is not part of the current working set, disable it for the session.

## Working sets

Servers belong to working sets. A working set is the group you actually use together for one kind of session. Sets do not mix. The concrete grouping of the connected servers lives in `mcp-configs/working-sets.json`. The named sets are:

- **evidence** for literature and trials work: PubMed, Consensus, Clinical Trials.
- **data** for storage and analysis: Supabase, Synapse.
- **comms** for scheduling and correspondence: Gmail, Calendar, Drive.
- **media** for generation, which almost never belongs in a research session: Higgsfield, HeyGen, Canva.
- **build** for site and product work: Wix.

## Session policy

- A grant-writing or protocol session enables **evidence** and nothing else unless a specific task needs more.
- Media servers stay off during any writing, analysis, or governance session. They are a separate mode.
- If a session needs two sets, that is allowed, but name why at the top of the working notes so the cost is visible.
- Review the enabled list before a long session the way you would clear a desk before work. The default posture is off, not on.

## Why this is a rule and not a preference

Context spent on idle tool schemas is context not spent on the trial protocol. The discipline is free and the failure is silent, which is exactly the profile of a constraint that belongs in an always-loaded rule.
