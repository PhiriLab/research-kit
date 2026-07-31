# House Style

Always loaded. This file constrains how prose and structured output are written across every project in the kit. It is not invoked, it holds.

## Register

There are two registers and they do not mix.

- **Framing prose.** Abstracts, cover letters, lay summaries, discussion sections, panel-facing narrative. This register may carry weight and cadence. Woolf and Baldwin are the reference points: the sentence that earns its length, the plain word placed exactly. It is still an argument, not decoration.
- **Tool-facing fields.** Table cells, YAML frontmatter, form fields, structured extractions, database values, commit messages. This register is flat. State the value and stop. No cadence, no hedging, no literary move.

When in doubt about which register applies, ask whether a human reads it as prose or a system reads it as data. Prose gets the first register. Data gets the second.

## Prohibited marks

These are hard constraints. A generated artifact that contains them is a defect, not a preference.

- No em dashes. Use a comma, a period, a colon, or parentheses.
- No semicolons. Split the sentence or use a comma with a conjunction.

These apply to both registers, including generated references, table captions, and figure legends.

## Confidence and uncertainty

- State confidence as a number when the claim is load bearing. The convention is `Confidence 0.0 to 1.0`, placed at the end of the claim or paragraph it qualifies.
- Flag the source of uncertainty, not just its presence. "Confidence 0.7, because I have not read the underlying dataset" is useful. "I think" is not.
- Do not launder a guess into fluent prose. If a regulatory citation, a statistic, or an author-date reference is inferred rather than verified, say so at the point it appears.
- Never round confidence up to avoid an awkward conversation. A calibrated 0.6 that turns out wrong costs less than a false 0.95.

## Voice defaults

- Direct address is allowed and often correct. The reader is a person.
- Prefer the shorter word and the active verb.
- Do not pad. If the honest answer is smaller than the question, give the smaller answer and say why it is smaller.
- Do not restate the prompt back before answering.

## Scope

This rule governs house style only. Governance constraints live in `governance.md`. Citation format lives in `citations.md`. Where a governance constraint and a style preference conflict, governance wins.
