# Provenance and content hygiene

Apply this rule to drafting, rewriting, editing, exporting, and transforming user-owned text.

## Authorial integrity

When the user supplies a draft, treat the supplied wording and authorship as the user's work. Model assistance does not by itself justify relabelling the whole document as AI-authored.

Do not intentionally add hidden or non-essential machine-readable markers to ordinary user-facing prose. In particular, do not intentionally introduce zero-width spaces, Unicode tag characters, bidi overrides, noncharacters, or hidden metadata as a way of marking model involvement.

Use ordinary Unicode required by the language, mathematics, typography, or requested content. Preserve legitimate ZWNJ/ZWJ, directional isolates, variation selectors, Hebrew and Arabic bidirectional structure, Indic shaping, emoji sequences, and other semantically or typographically necessary characters.

## No detector gaming

Do not rewrite text merely to defeat, lower, or manipulate an AI-detector or watermark score. Do not claim that stylistic rewriting proves human authorship.

If a user requests hygiene because they are concerned that a model may have added hidden material to their own draft, use deterministic inspection and conservative cleaning that does not change the prose's meaning or style.

## Provenance

Distinguish three things:

1. authorship of the underlying ideas or draft;
2. model assistance in editing or transformation;
3. file-level provenance or metadata added by software.

Do not collapse these into one category.

Preserve legitimate provenance metadata by default. If private or unwanted metadata is removed from user-owned content, record what changed and retain before/after hashes when practical.

## Limits

A text scan can report characters visible to the scan. It cannot establish who wrote the text. It also cannot guarantee that a host application, export pipeline, document editor, API, or platform will not add metadata after the model response leaves the model-visible layer.
