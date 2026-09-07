"""Regression checks for public release versioning."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VersionConsistencyTests(unittest.TestCase):
    def test_protocol_references_match(self):
        versions = []
        for path in ("SPEC.md", "skills/6x6/references/SPEC.md"):
            text = (ROOT / path).read_text(encoding="utf-8")
            match = re.search(r"^Version: (\d+\.\d+\.\d+)$", text, re.M)
            self.assertIsNotNone(match, path)
            versions.append(match.group(1))
        self.assertEqual(versions[0], versions[1])

    def test_package_release_metadata(self):
        skill = (ROOT / "skills/6x6/SKILL.md").read_text(encoding="utf-8")
        match = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', skill, re.M)
        self.assertIsNotNone(match)
        version = match.group(1)
        self.assertIn(f"v{version} stable release", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(f"## [{version}]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    def test_versioning_policy_exists(self):
        self.assertTrue((ROOT / "docs/RELEASE_VERSIONING.md").is_file())


if __name__ == "__main__":
    unittest.main()
