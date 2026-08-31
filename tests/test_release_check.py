import tempfile
import unittest
from pathlib import Path

from tools.release_check import REQUIRED, run, skill_version


class ReleaseCheckTests(unittest.TestCase):
    def test_skill_version_reads_metadata_version(self):
        text = '---\nmetadata:\n  version: "0.3.0-rc1"\n---\n'
        self.assertEqual(skill_version(text), "0.3.0-rc1")

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


if __name__ == "__main__":
    unittest.main()
