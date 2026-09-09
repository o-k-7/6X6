import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "6x6"


class PluginPackageTests(unittest.TestCase):
    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_manifests_are_valid_json(self):
        paths = (
            PLUGIN / "plugin.json",
            PLUGIN / ".codex-plugin" / "plugin.json",
            PLUGIN / ".claude-plugin" / "plugin.json",
            ROOT / ".agents" / "plugins" / "marketplace.json",
            ROOT / ".claude-plugin" / "marketplace.json",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertIsInstance(self.load_json(path), dict)

    def test_openai_manifests_match(self):
        portable = self.load_json(PLUGIN / "plugin.json")
        codex = self.load_json(PLUGIN / ".codex-plugin" / "plugin.json")
        self.assertEqual(portable, codex)

    def test_manifest_identity_and_version_match_skill(self):
        manifest = self.load_json(PLUGIN / "plugin.json")
        skill = (ROOT / "skills" / "6x6" / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["name"], "6x6")
        self.assertEqual(manifest["version"], "1.0.2")
        self.assertIn('version: "1.0.2"', skill)

    def test_packaged_skill_matches_canonical_skill(self):
        pairs = (
            ("SKILL.md", "SKILL.md"),
            ("references/SPEC.md", "references/SPEC.md"),
            ("agents/openai.yaml", "agents/openai.yaml"),
        )
        for source, packaged in pairs:
            with self.subTest(path=source):
                self.assertEqual(
                    (ROOT / "skills" / "6x6" / source).read_bytes(),
                    (PLUGIN / "skills" / "6x6" / packaged).read_bytes(),
                )

    def test_marketplaces_reference_local_package(self):
        openai = self.load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
        claude = self.load_json(ROOT / ".claude-plugin" / "marketplace.json")
        self.assertEqual(openai["plugins"][0]["source"]["path"], "./plugins/6x6")
        self.assertEqual(claude["plugins"][0]["source"], "./plugins/6x6")
        self.assertEqual(claude["plugins"][0]["name"], "6x6")

    def test_assets_are_local_and_present(self):
        interface = self.load_json(PLUGIN / "plugin.json")["interface"]
        for field in ("composerIcon", "logo", "logoDark"):
            path = PLUGIN / interface[field].removeprefix("./")
            with self.subTest(field=field):
                self.assertTrue(path.is_file())
                self.assertGreater(path.stat().st_size, 0)

    def test_legal_files_match_repository(self):
        for name in ("LICENSE", "PRIVACY.md", "LEGAL.md"):
            with self.subTest(path=name):
                self.assertEqual(
                    (ROOT / name).read_bytes(),
                    (PLUGIN / name).read_bytes(),
                )

    def test_package_has_no_executable_or_network_component(self):
        forbidden = {"hooks", "mcpServers", "apps"}
        manifest = self.load_json(PLUGIN / "plugin.json")
        self.assertTrue(forbidden.isdisjoint(manifest))
        self.assertFalse((PLUGIN / ".mcp.json").exists())
        self.assertFalse((PLUGIN / "hooks.json").exists())


if __name__ == "__main__":
    unittest.main()
