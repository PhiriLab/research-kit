---
name: provenance-content-hygiene
description: Inspect and conservatively clean user-owned drafts and files for hidden Unicode and provenance-bearing metadata without changing meaning or rewriting to evade AI detection. Use when preparing, reviewing, publishing, exporting, or transferring a draft between ChatGPT, Claude, Gemini, editors, or document tools, especially when the user wants authorial integrity, minimal hidden-character hygiene, provenance inspection, or a before/after audit trail.
---

# Provenance & Content Hygiene

Protect the user's authorship and document integrity without pretending that any technical cleanup proves who wrote a text.

## Core boundary

This skill is for provenance-preserving hygiene, not detector evasion.

- Preserve the user's wording, claims, citations, names, numbers, structure, and voice unless the user separately asks for editing.
- Do not paraphrase, back-translate, vary tokens, or "humanize" text merely to alter AI-detector or watermark scores.
- Do not state that cleaned text is "AI-free", "human-written", or incapable of being classified as AI-generated.
- Do not infer authorship from the presence or absence of invisible characters, metadata, C2PA, or any detector score.
- Work only on content the user owns or is authorized to process.

## Default workflow

1. Inspect first.
2. Report exactly what was found.
3. Preserve legitimate Unicode and legitimate provenance by default.
4. Clean only the conservative text set unless the user explicitly requests a stronger operation.
5. Produce a before/after SHA-256 record when a file is changed.
6. State what changed and what was deliberately preserved.

The bundled script is `scripts/provenance_hygiene.py`.

### Inspect a file

```bash
python3 scripts/provenance_hygiene.py inspect PATH --json
```

### Conservatively clean a text file

```bash
python3 scripts/provenance_hygiene.py clean PATH --output PATH.cleaned --audit PATH.cleaned.audit.json
```

### Inspect pasted text

Write the text to a UTF-8 temporary `.txt` or `.md` file without altering it, then inspect that file. Delete the temporary file after use when appropriate.

## Unicode policy

The default cleaner removes only characters that are usually accidental or covert in ordinary prose and that can be removed without changing normal language shaping:

- U+200B ZERO WIDTH SPACE
- U+FEFF ZERO WIDTH NO-BREAK SPACE when it appears inside decoded text

The following are audit-only by default and must not be stripped automatically:

- U+200C ZERO WIDTH NON-JOINER
- U+200D ZERO WIDTH JOINER
- left-to-right and right-to-left marks
- bidi embeddings, overrides, and isolates
- variation selectors
- Unicode tag characters
- noncharacters and reserved default-ignorable characters

This is deliberate. ZWNJ/ZWJ and directional controls can be legitimate in Persian, Arabic, Indic scripts, Hebrew mixed-direction text, emoji sequences, mathematical notation, and specialist typography.

## File provenance policy

For binary and container formats, inspect without destructive cleaning by default.

The bundled inspector can report:

- SHA-256 and byte size
- likely C2PA/XMP/EXIF marker presence by conservative byte signatures
- OOXML/ODF/EPUB metadata-bearing package paths such as `docProps/`, `customXml/`, and `META-INF/`

Do not remove C2PA or document metadata automatically. Provenance can be evidence. If the user explicitly asks to remove private metadata from a file they own, use a separately reviewed tool and retain a before/after audit record.

## When producing new text

When this skill is active and you are drafting text directly:

- do not intentionally insert non-essential invisible Unicode, tag characters, bidi overrides, or hidden metadata;
- use ordinary Unicode required by the requested language and typography;
- preserve legitimate Hebrew, Arabic, Indic, emoji, mathematical, and multilingual shaping characters;
- if the host platform may add provenance outside the model-visible text, do not claim control over that platform layer.

## Report language

Use precise language such as:

- "No characters in the conservative removal set were detected."
- "Directional controls were detected and preserved for review."
- "The cleaned file differs only by removal of U+200B characters."
- "This audit does not establish whether the text was written by a human or an AI system."

Avoid claims that exceed what was actually inspected.
