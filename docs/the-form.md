# The Form

## What was taken from ECC, and what was not

ECC is a working grammar for a TypeScript product team shipping SaaS. Its centre of gravity is React, Next.js, Playwright, package managers, coverage thresholds, and pull-request hygiene. Read against a Python statistical research stack, most of it does not land. The build-error resolver is tuned for cryptic compiler and bundler failures. The frontend-patterns skill assumes a component tree. The end-to-end runner assumes a browser.

So the content was left behind. Four pieces of the grammar were taken:

1. **Rules as persistent constraint.** Small, always-loaded markdown that holds without being invoked. This is the highest-return component and it has almost nothing to do with software. See `rules/`.
2. **Verification loops.** Checkpoint versus continuous evaluation, and pass@k read as stability rather than as a pass mark. See `verification/`.
3. **Memory persistence, as a pattern.** Continuity keyed to project, not to date. See `hooks/memory-persistence/`.
4. **MCP discipline.** Fewer than ten servers enabled per session, grouped into working sets. See `rules/mcp-discipline.md` and `mcp-configs/working-sets.json`.

## What was not carried over

These parts of ECC were not brought across, because they serve a software-engineering surface this kit does not have today. None of this is a judgement that they are unwanted. Any of them can be pulled in later if a surface appears that needs them.

- The test-driven-development workflow and its coverage threshold.
- The backend and frontend pattern libraries.
- The browser end-to-end runner (Playwright) and the build-error resolver. These matter only when there is a web front end to drive.
- The git-workflow rules.

One item carries a specific warning if it is ever adopted. ECC's security-review skill is competent web-application security content. It is not health information governance. It says nothing about national health-data security standards, clinical-safety cases, or cross-border regulatory position. Adopting it could leave a session feeling covered when it is not, and that is worse than having nothing. `rules/governance.md` names the gap rather than papering over it.

## The thing nobody has built

What ECC demonstrates is that a serious practitioner can encode a decade of tacit workflow into portable, inspectable text, and that doing so compounds. The same has not been done for regulated health research. There is no published rules and skills layer for trial protocol development, for cultural adaptation of interventions, for target trial emulation, or for the specific discipline of writing to a funding panel.

The material for it already exists, scattered across artifacts already built. The value of going to ECC was never what could be taken from it. It was seeing the form clearly enough to build the same thing in a domain where the form does not yet exist.

This repository is the start of that. The rules directory is the first afternoon. Confidence 0.85, with the standing caveat that the codebase composition is inferred from description rather than read directly.
