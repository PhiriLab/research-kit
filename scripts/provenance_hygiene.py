#!/usr/bin/env python3
"""Conservative provenance and hidden-Unicode hygiene for user-owned content."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
import zipfile
from collections import Counter
from io import BytesIO
from pathlib import Path

TEXT_SUFFIXES = {
    ".txt", ".md", ".markdown", ".csv", ".json", ".jsonl", ".yaml", ".yml",
    ".toml", ".ini", ".cfg", ".py", ".js", ".jsx", ".ts", ".tsx", ".html",
    ".htm", ".xml", ".tex", ".rst", ".sql", ".css", ".scss", ".sh", ".zsh",
    ".bash", ".ps1",
}
ZIP_CONTAINER_SUFFIXES = {".docx", ".xlsx", ".pptx", ".odt", ".ods", ".odp", ".epub"}
REMOVE_ALWAYS = {0x200B}
REMOVE_INTERIOR_ONLY = {0xFEFF}
AUDIT_NAMED = {
    0x00AD: "SOFT HYPHEN",
    0x200C: "ZERO WIDTH NON-JOINER",
    0x200D: "ZERO WIDTH JOINER",
    0x200E: "LEFT-TO-RIGHT MARK",
    0x200F: "RIGHT-TO-LEFT MARK",
    0x202A: "LEFT-TO-RIGHT EMBEDDING",
    0x202B: "RIGHT-TO-LEFT EMBEDDING",
    0x202C: "POP DIRECTIONAL FORMATTING",
    0x202D: "LEFT-TO-RIGHT OVERRIDE",
    0x202E: "RIGHT-TO-LEFT OVERRIDE",
    0x2060: "WORD JOINER",
    0x2066: "LEFT-TO-RIGHT ISOLATE",
    0x2067: "RIGHT-TO-LEFT ISOLATE",
    0x2068: "FIRST STRONG ISOLATE",
    0x2069: "POP DIRECTIONAL ISOLATE",
}
BINARY_MARKERS = {
    "c2pa": (b"c2pa", b"jumb"),
    "content_credentials": (b"Content Credentials",),
    "xmp": (b"<x:xmpmeta", b"http://ns.adobe.com/xap/1.0/"),
    "exif": (b"Exif\x00\x00",),
}
CONTAINER_METADATA_PREFIXES = ("docProps/", "customXml/", "META-INF/")
CONTAINER_METADATA_NAMES = {"meta.xml", "content.opf"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_noncharacter(cp: int) -> bool:
    return 0xFDD0 <= cp <= 0xFDEF or (cp & 0xFFFF) in {0xFFFE, 0xFFFF}


def audit_class(cp: int) -> str | None:
    if cp in REMOVE_ALWAYS:
        return "removable_zero_width"
    if cp in REMOVE_INTERIOR_ONLY:
        return "interior_bom_or_zw_nbsp"
    if cp in AUDIT_NAMED:
        return "preserve_review"
    if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
        return "variation_selector"
    if 0xE0000 <= cp <= 0xE007F:
        return "unicode_tag"
    if is_noncharacter(cp):
        return "noncharacter"
    if unicodedata.category(chr(cp)) == "Cf":
        return "other_format_control"
    return None


def inspect_text(text: str, max_positions: int = 100) -> dict:
    counts: Counter[tuple[int, str]] = Counter()
    positions: list[dict] = []
    for index, char in enumerate(text):
        cp = ord(char)
        cls = audit_class(cp)
        if cls is None:
            continue
        counts[(cp, cls)] += 1
        if len(positions) < max_positions:
            positions.append({
                "index": index,
                "codepoint": f"U+{cp:04X}",
                "name": unicodedata.name(char, AUDIT_NAMED.get(cp, "UNNAMED")),
                "class": cls,
                "default_action": "remove"
                if cp in REMOVE_ALWAYS or (cp in REMOVE_INTERIOR_ONLY and index > 0)
                else "preserve_review",
            })
    removable = sum(
        1 for i, char in enumerate(text)
        if ord(char) in REMOVE_ALWAYS or (ord(char) in REMOVE_INTERIOR_ONLY and i > 0)
    )
    findings = [
        {
            "codepoint": f"U+{cp:04X}",
            "name": unicodedata.name(chr(cp), AUDIT_NAMED.get(cp, "UNNAMED")),
            "class": cls,
            "count": count,
        }
        for (cp, cls), count in sorted(counts.items())
    ]
    return {
        "characters": len(text),
        "findings": findings,
        "positions": positions,
        "positions_truncated": sum(counts.values()) > len(positions),
        "conservative_removable_count": removable,
        "authorship_inference": "not_supported",
    }


def clean_text(text: str) -> tuple[str, dict]:
    kept: list[str] = []
    removed: Counter[int] = Counter()
    for index, char in enumerate(text):
        cp = ord(char)
        if cp in REMOVE_ALWAYS or (cp in REMOVE_INTERIOR_ONLY and index > 0):
            removed[cp] += 1
        else:
            kept.append(char)
    return "".join(kept), {
        "removed": [
            {
                "codepoint": f"U+{cp:04X}",
                "name": unicodedata.name(chr(cp), AUDIT_NAMED.get(cp, "UNNAMED")),
                "count": count,
            }
            for cp, count in sorted(removed.items())
        ],
        "removed_total": sum(removed.values()),
        "policy": "conservative",
    }


def inspect_binary(data: bytes, suffix: str) -> dict:
    lowered = data.lower()
    report = {
        "markers": {
            name: any(marker.lower() in lowered for marker in markers)
            for name, markers in BINARY_MARKERS.items()
        },
        "marker_note": "Byte-signature matches are indicators only. Absence does not prove absence of provenance metadata.",
    }
    if suffix in ZIP_CONTAINER_SUFFIXES and data.startswith(b"PK"):
        try:
            with zipfile.ZipFile(BytesIO(data)) as archive:
                names = archive.namelist()
                metadata = [
                    name for name in names
                    if name.startswith(CONTAINER_METADATA_PREFIXES)
                    or name.rsplit("/", 1)[-1] in CONTAINER_METADATA_NAMES
                ]
                report["container_metadata_paths"] = metadata[:200]
                report["container_metadata_paths_truncated"] = len(metadata) > 200
        except (zipfile.BadZipFile, OSError):
            report["container_error"] = "invalid_or_unreadable_zip_container"
    return report


def inspect_file(path: Path) -> dict:
    data = path.read_bytes()
    base = {
        "path": str(path),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
        "suffix": path.suffix.lower(),
        "authorship_inference": "not_supported",
    }
    if path.suffix.lower() in TEXT_SUFFIXES:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            base["kind"] = "binary_or_non_utf8"
            base["inspection"] = inspect_binary(data, path.suffix.lower())
            return base
        base["kind"] = "text"
        base["inspection"] = inspect_text(text)
        return base
    if b"\x00" not in data[:4096]:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            pass
        else:
            base["kind"] = "text"
            base["inspection"] = inspect_text(text)
            return base
    base["kind"] = "binary_or_container"
    base["inspection"] = inspect_binary(data, path.suffix.lower())
    return base


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def clean_file(path: Path, output: Path, audit_path: Path | None) -> dict:
    before = path.read_bytes()
    if path.suffix.lower() not in TEXT_SUFFIXES:
        raise ValueError(
            "conservative clean supports UTF-8 text-like files only; binary/container files are inspect-only"
        )
    try:
        text = before.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("conservative clean requires UTF-8 text") from exc
    cleaned, changes = clean_text(text)
    after = cleaned.encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(after)
    audit = {
        "source": str(path),
        "output": str(output),
        "policy": "provenance-preserving-conservative",
        "before": {"bytes": len(before), "sha256": sha256_bytes(before)},
        "after": {"bytes": len(after), "sha256": sha256_bytes(after)},
        "changed": before != after,
        "changes": changes,
        "preserved_by_default": [
            "U+200C ZERO WIDTH NON-JOINER",
            "U+200D ZERO WIDTH JOINER",
            "bidi direction controls",
            "variation selectors",
            "Unicode tag characters",
            "binary/container provenance metadata",
        ],
        "authorship_inference": "not_supported",
    }
    if audit_path is not None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(audit_path, audit)
    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect or conservatively clean hidden Unicode and provenance indicators."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect", help="Inspect without modification")
    inspect_parser.add_argument("path", type=Path)
    inspect_parser.add_argument("--json", action="store_true")
    clean_parser = subparsers.add_parser("clean", help="Conservatively clean UTF-8 text")
    clean_parser.add_argument("path", type=Path)
    output_group = clean_parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument("--output", type=Path)
    output_group.add_argument("--in-place", action="store_true")
    clean_parser.add_argument("--audit", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            report = inspect_file(args.path)
            if args.json:
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                print(f"{report['kind']}: {report['path']}")
                print(f"sha256: {report['sha256']}")
                print(json.dumps(report["inspection"], indent=2, ensure_ascii=False))
            return 0
        output = args.path if args.in_place else args.output
        print(json.dumps(clean_file(args.path, output, args.audit), indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
