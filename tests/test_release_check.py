import tempfile
import unittest
from pathlib import Path

from tools.release_check import REQUIRED, run, skill_version


class ReleaseCheckTests(unittest.TestCase):
    def test_skill_version_reads_metadata_version(self):
        text = '---\nmetadata:\n  version: "1.0.0"\n---\n'
        self.assertEqual(skill_version(text), "1.0.0")

    def test_skill_version_missing_returns_none(self):
        self.assertIsNone(skill_version("---\nname: 6x6\n---\n"))

    def test_empty_repository_reports_required_files(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = run(Path(directory))
        self.assertGreaterEqual(len(errors), len(REQUIRED))
        self.assertIn("missing required file: README.md", errors)

    def test_root_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text("bad layout", encoding="utf-8")
            errors = run(root)
        self.assertIn("ambiguous root SKILL.md must not exist", errors)

    def test_bundled_spec_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SPEC.md").write_text("root", encoding="utf-8")
            bundled = root / "skills/6x6/references/SPEC.md"
            bundled.parent.mkdir(parents=True)
            bundled.write_text("different", encoding="utf-8")
            errors = run(root)
        self.assertIn("bundled Skill SPEC must exactly match root SPEC.md", errors)

    def test_new_hardening_assets_are_required(self):
        self.assertIn("tools/enforce.py", REQUIRED)
        self.assertIn("tools/live_acceptance.py", REQUIRED)
        self.assertIn("docs/MODEL_ACCEPTANCE.md", REQUIRED)

    def test_invalid_evidence_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "broken.json").write_text("truncated", encoding="utf-8")
            errors = run(root)
        self.assertIn("invalid evidence JSON: broken.json", errors)

    def test_non_object_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "evidence"
            evidence.mkdir()
            (evidence / "array.json").write_text("[]", encoding="utf-8")
            errors = run(root)
        self.assertIn("evidence must be a JSON object: array.json", errors)


if __name__ == "__main__":
    unittest.main()
