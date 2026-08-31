import tempfile
import unittest
from pathlib import Path

from tools.security_check import scan


class SecurityCheckTests(unittest.TestCase):
    def _scan_files(self, files: dict[str, str]):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, content in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return scan(root)

    def test_clean_python_is_allowed(self):
        findings = self._scan_files({"tool.py": "from pathlib import Path\nprint(Path('.'))\n"})
        self.assertEqual(findings, [])

    def test_shell_execution_is_rejected(self):
        findings = self._scan_files({"tool.py": "import os\nos.system('echo unsafe')\n"})
        self.assertTrue(any(item.category == "shell execution" for item in findings))

    def test_process_import_is_rejected(self):
        findings = self._scan_files({"tool.py": "import subprocess as sp\nprint(sp)\n"})
        self.assertTrue(any(item.category == "network or process import" for item in findings))

    def test_network_client_is_rejected(self):
        findings = self._scan_files({"tool.py": "import socket\nsocket.create_connection(('example.com', 443))\n"})
        self.assertTrue(any(item.category in {"network or process import", "network client"} for item in findings))

    def test_dynamic_execution_is_rejected(self):
        findings = self._scan_files({"tool.py": "exec('print(1)')\n"})
        self.assertTrue(any(item.category == "dynamic execution" for item in findings))

    def test_private_key_is_rejected(self):
        findings = self._scan_files({"secret.txt": "-----BEGIN PRIVATE KEY-----\nnot-real\n"})
        self.assertTrue(any(item.category == "private key" for item in findings))

    def test_github_token_shape_is_rejected(self):
        findings = self._scan_files({"secret.txt": "ghp_123456789012345678901234567890123456\n"})
        self.assertTrue(any(item.category == "github token" for item in findings))

    def test_extensionless_text_is_scanned(self):
        findings = self._scan_files({"SECRETS": "AKIA1234567890ABCDEF\n"})
        self.assertTrue(any(item.category == "aws access key" for item in findings))


if __name__ == "__main__":
    unittest.main()
