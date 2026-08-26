import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "provenance_hygiene.py"
SPEC = importlib.util.spec_from_file_location("provenance_hygiene", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class ProvenanceHygieneTests(unittest.TestCase):
    def test_removes_only_conservative_set(self):
        cleaned, report = module.clean_text("A\u200bB\u200cC\u200dD")
        self.assertEqual(cleaned, "AB\u200cC\u200dD")
        self.assertEqual(report["removed_total"], 1)

    def test_preserves_leading_bom_but_removes_interior_feff(self):
        cleaned, report = module.clean_text("\ufeffTitle\ufeffBody")
        self.assertEqual(cleaned, "\ufeffTitleBody")
        self.assertEqual(report["removed_total"], 1)

    def test_hebrew_directional_controls_are_audit_only(self):
        text = "\u2067שלום\u2069"
        classes = {finding["class"] for finding in module.inspect_text(text)["findings"]}
        self.assertIn("preserve_review", classes)
        self.assertEqual(module.clean_text(text)[0], text)

    def test_binary_clean_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.png"
            source.write_bytes(b"\x89PNG\r\n\x1a\n")
            with self.assertRaises(ValueError):
                module.clean_file(source, Path(directory) / "out.png", None)

    def test_audit_contains_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "draft.md"
            output = Path(directory) / "draft.cleaned.md"
            audit = Path(directory) / "audit.json"
            source.write_text("A\u200bB", encoding="utf-8")
            report = module.clean_file(source, output, audit)
            self.assertTrue(report["changed"])
            self.assertEqual(output.read_text(encoding="utf-8"), "AB")
            saved = json.loads(audit.read_text(encoding="utf-8"))
            self.assertEqual(saved["changes"]["removed_total"], 1)
            self.assertEqual(len(saved["before"]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
