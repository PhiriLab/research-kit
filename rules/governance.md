# Governance

Always loaded. This is the highest-consequence rule in the kit. It catches disclosure and residency failures at the point of generation, before anything reaches a prompt, a commit, or a hosted service. Where this rule conflicts with any other rule or any convenience, this rule wins.

## Identifiers that must never enter a prompt or a committed file

The following never appear in an LLM prompt, a tool call, a commit, a log, or any file tracked in this repository. Not in examples, not in test fixtures, not in a comment.

- Participant identifiers of any kind, including names, dates of birth, national or local health-record numbers, and any local record number.
- Study or ethics approval reference numbers.
- Site codes and any string that resolves to a single recruiting site.
- Free-text clinical notes that could re-identify an individual.
- Any combination of fields that is identifying in aggregate even when each field alone is not.

### What to do instead

- Replace the identifier with a pseudonymised token that is meaningless outside the secure store, for example `PT-<opaque>` or `SITE-<opaque>`.
- Keep the mapping between token and real value only in the approved secure environment, never in this repository and never in a prompt.
- If a task genuinely requires the real value, that task does not run through this kit. Stop and move it to the approved environment.

A committed identifier is a reportable event, not a bug to quietly fix. Treat a near miss as a signal that the workflow, not the operator, needs changing.

## Data residency

Multi-jurisdiction work carries residency and regulatory constraints that a single-country workflow does not satisfy. Data location and processing location both matter.

- Do not assume a lawful basis in one jurisdiction transfers to another. Cross-border transfer of participant data needs an explicit, recorded lawful basis for each jurisdiction it touches.
- Identify the governing data-protection instrument and the relevant regulator for every jurisdiction in scope, and record the verification before any data from that jurisdiction is processed or moved. Do not rely on assumption or memory here. Confidence in an uncited residency claim is 0.0 until it is checked against the instrument.
- When a session touches more than one jurisdiction, name the jurisdictions at the top of the working notes so residency is visible, not implied.

## What this rule does not cover

This rule is disclosure and residency. It is not a health information governance certification. It does not stand in for any national health-data security standard, a clinical-safety case, or a formal Data Protection Impact Assessment. Do not read a green result here as evidence of any of those. A separate, competent governance review is still required, and the absence of one is a gap to name, not to paper over. Confidence 0.9 that treating this rule as sufficient coverage would be the more dangerous error than having no rule at all.

## Precedence

Governance outranks house style, citation format, velocity, and deadline. If honoring this rule means an artifact is late or unfinished, it is late or unfinished.
