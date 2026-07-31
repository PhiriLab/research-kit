# Verification

The concept is not new here. Evaluation tooling already runs in the wider setup, so this piece adds a distinction that has not yet been operationalised, and it connects to a grounding step that already exists.

## Checkpoint evaluation versus continuous evaluation

- **Checkpoint evaluation** runs at a boundary. Before a submission, before a costing is locked, before capital moves. It answers "is this good enough to pass this gate." It is a pass mark.
- **Continuous evaluation** runs on every change. It answers "did this change make anything worse." It is a regression signal, not a gate.

Both are needed and they are not the same instrument. A checkpoint eval that runs continuously becomes noise. A continuous eval that only runs at checkpoints misses the silent drift between them.

## pass@k as a stability measure

pass@k is treated here as stability, not as a pass mark. Running the same evaluation k times and reading the spread tells you whether a result is robust or lucky. A claim that passes once at k=1 and fails three times at k=4 is not a passing claim, it is an unstable one.

This transfers directly to any stopping rule. When a programme is held in a pre-registered or demo phase because evidence is not yet strong enough to move ahead, a formal harness gives that instinct a number instead of a feeling. Confidence 0.8 that this is the most technically transferable piece.

## Grounding extracted skills

Extracting a skill from a source text carries a specific risk: a badly extracted skill propagates silently into everything downstream that loads it. A wrong statement of a statistical method's assumptions, drawn from a manual, is the failure with the longest blast radius.

This kit does not reinvent that check. The grounding step is the existing `source-to-grounded` skill, which grounds an extracted skill against its source. What this directory adds is the evaluation layer around it:

1. The `source-to-grounded` skill grounds the extracted claim against the source, not against a paraphrase.
2. The skill runs at k greater than 1 on a small held-out set and the spread is recorded.
3. A skill that fails grounding or shows an unstable spread is quarantined, not merged. A quarantined skill never loads.

## Status

This directory holds the contract, not yet the harness. The harness wraps the existing evaluation tooling and the existing `source-to-grounded` skill rather than replacing either. Wiring the quarantine gate is the next step, because an unverified skill is the failure with the longest reach. Confidence 0.75.
