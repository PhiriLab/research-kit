# PhiriLab provenance and content hygiene

Protect the user's authorial integrity when drafting, editing, rewriting, exporting, or reviewing user-owned material.

Do not intentionally add non-essential invisible Unicode, Unicode tag characters, bidi overrides, noncharacters, or hidden metadata to ordinary prose. Preserve Unicode that is legitimate for the language or typography, including ZWNJ/ZWJ, directional isolates, Hebrew and Arabic bidirectional structure, Indic shaping, variation selectors, emoji sequences, and mathematical notation.

When the user supplies a draft, do not treat model assistance as evidence that the entire document is AI-authored. Distinguish the user's underlying authorship from later model assistance and from software-added file metadata.

Do not paraphrase, back-translate, or "humanize" text merely to change an AI-detector or watermark score. Deterministic hygiene should preserve the user's wording and meaning.

For a user-owned file that needs inspection, use the installed PhiriLab command when shell execution is available:

`python3 ~/.phirilab/provenance-hygiene/provenance_hygiene.py inspect PATH --json`

For conservative text cleaning, first inspect, then use:

`python3 ~/.phirilab/provenance-hygiene/provenance_hygiene.py clean PATH --output PATH.cleaned --audit PATH.cleaned.audit.json`

Binary and container files are inspect-only by default. Do not remove C2PA or document provenance automatically.

Never claim that a clean scan proves human authorship or that a host platform cannot add metadata after generation.
