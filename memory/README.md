# memory

Per-project session state. One directory per live thread, one `state.md` per thread, written by `scripts/memory/session.py`.

```
memory/
├── <project-a>/state.md
├── <project-b>/state.md
└── <project-c>/state.md
```

Project directory names are chosen by the operator, one per live project.

A state file summarises what was done and what remains open. It is not a transcript and it carries no data. `rules/governance.md` applies in full: no participant identifier, no approval reference, no site code, ever. Governance outranks memory.
