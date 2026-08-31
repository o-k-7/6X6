import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "6x6"
SKILL_MD = SKILL_DIR / "SKILL.md"
ALLOWED_TOP_LEVEL_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}


def parse_top_level_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter must be closed")

    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


class AgentSkillPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL_MD.read_text(encoding="utf-8")
        cls.meta = parse_top_level_frontmatter(cls.text)

    def test_canonical_skill_directory_matches_name(self):
        self.assertEqual(SKILL_DIR.name, self.meta["name"])

    def test_name_matches_agent_skills_constraints(self):
        name = self.meta["name"]
        self.assertGreaterEqual(len(name), 1)
        self.assertLessEqual(len(name), 64)
        self.assertEqual(name, name.lower())
        self.assertFalse(name.startswith("-") or name.endswith("-"))
        self.assertNotIn("--", name)
        self.assertRegex(name, r"^[a-z0-9-]+$")

    def test_required_fields_exist(self):
        self.assertTrue(self.meta.get("name"))
        self.assertTrue(self.meta.get("description"))

    def test_only_spec_fields_are_used(self):
        self.assertFalse(set(self.meta) - ALLOWED_TOP_LEVEL_FIELDS)

    def test_description_length_is_valid(self):
        description = self.meta["description"]
        self.assertLessEqual(len(description), 1024)

    def test_reference_exists(self):
        self.assertTrue((SKILL_DIR / "references" / "SPEC.md").is_file())

    def test_skill_body_stays_compact(self):
        self.assertLess(len(self.text.splitlines()), 500)

    def test_reference_is_relative_and_one_level_deep(self):
        self.assertIn("`references/SPEC.md`", self.text)
        self.assertNotRegex(self.text, re.compile(r"references/[^/]+/"))


if __name__ == "__main__":
    unittest.main()
