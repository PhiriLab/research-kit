# Memory Persistence

The implementation is thin on purpose. You could write it better, and you should. What matters is the pattern, not the code.

## The problem

A chat window has the wrong shape for this work. A funding application can span weeks. A costing exercise can run across many funders and months. A session boundary corresponds to nothing real. Left alone, every new session starts cold and re-derives context that was settled a week ago.

## The pattern

Impose continuity the tool does not have by default. Key it to project, not to date, so each live thread carries its own state.

- `SessionStart` loads `memory/<project>/state.md` and prepends the always-loaded rules from `../../rules/`.
- `SessionEnd` records where work stopped and what remains open, back into the same file.

One thread per live project, named by the operator. Add a thread when a project goes live, retire it when the project closes.

## Reference implementation

`scripts/memory/session.py` is a minimal, correct starting point. It reads and writes a per-project markdown state file and nothing else. It sends nothing anywhere. Point the hook definitions in `hooks.json` at it, or replace it with your own once the shape is proven.

## The one hard constraint

A state file is a committed artifact in the general case, so `governance.md` applies in full. No participant identifier, no approval reference, no site code, ever, in a state file. A state file summarises what was done and what is open. It does not carry data. Governance outranks memory.
