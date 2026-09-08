import unittest

from tools.validate_open_evidence import REQUIRED_SCENARIOS, validate


def evidence() -> dict:
    scenarios = [{
        "id": scenario_id,
        "prompt": "Synthetic prompt",
        "instruction_only": {"raw_final_output": "Answer", "score": {"passed": True}},
        "host_enforced": {"status": "pass", "released": True, "raw_final_output": "Answer", "score": {"passed": True}},
    } for scenario_id in REQUIRED_SCENARIOS]
    models = [{
        "provider": f"provider-{number}", "model": "model", "model_digest": "digest",
        "protocol_sha256": "0" * 64, "timestamp": "2026-09-08T00:00:00+00:00",
        "runtime": {}, "scenarios": scenarios,
    } for number in range(8)]
    return {"schema_version": 4, "models": models, "summary": {
        "requested_models": 8, "models_executed": 8, "instruction_only_passed": 64,
        "host_enforced_passed": 64, "blocked": 0, "infrastructure_errors": 0,
        "scenario_total": 64,
    }}


class OpenEvidenceTests(unittest.TestCase):
    def test_complete_evidence_passes(self):
        self.assertEqual(validate(evidence()), [])

    def test_summary_mismatch_fails(self):
        data = evidence()
        data["summary"]["host_enforced_passed"] = 63
        self.assertIn("summary does not match scenario records", validate(data))

    def test_blocked_release_fails(self):
        data = evidence()
        host = data["models"][0]["scenarios"][0]["host_enforced"]
        host.update({"status": "blocked", "released": True})
        self.assertTrue(any("blocked output was released" in error for error in validate(data)))


if __name__ == "__main__":
    unittest.main()
