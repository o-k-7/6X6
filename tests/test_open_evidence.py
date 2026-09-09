import unittest

from tools.validate_open_evidence import REQUIRED_PROVIDERS, REQUIRED_SCENARIOS, validate


def evidence() -> dict:
    scenarios = [{
        "id": scenario_id,
        "mode": "full" if scenario_id == "full" else "expand" if scenario_id == "expand" else "signal",
        "prompt": "Synthetic prompt",
        "instruction_only": {
            "raw_final_output": "Answer", "thinking_present": False, "done_reason": "stop",
            "score": {"nonempty": True, "passed": True},
        },
        "host_enforced": {
            "status": "pass", "released": True, "raw_final_output": "Answer",
            "attempts": [{"number": 1, "nonempty": True, "semantic_ok": True, "reflowed": False}],
            "provider_attempts": [{"thinking_present": False, "done_reason": "stop"}],
            "score": {"nonempty": True, "passed": True},
        },
    } for scenario_id in REQUIRED_SCENARIOS]
    models = [{
        "provider": provider, "model": "model", "model_digest": "1" * 64,
        "protocol_sha256": "0" * 64, "timestamp": "2026-09-08T00:00:00+00:00",
        "runtime": {"ollama": {}, "num_predict": 768, "num_ctx": 4096, "temperature": 0},
        "baseline": {
            "raw_final_output": "Answer", "thinking_present": False,
            "score": {"nonempty": True, "passed": True},
        },
        "scenarios": scenarios,
    } for provider in REQUIRED_PROVIDERS]
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

    def test_incomplete_provider_matrix_fails(self):
        data = evidence()
        data["models"].pop()
        self.assertIn("models must contain exactly 8 records", validate(data))

    def test_missing_attempt_metadata_fails(self):
        data = evidence()
        del data["models"][0]["scenarios"][0]["host_enforced"]["attempts"]
        self.assertTrue(any("missing attempt metadata" in error for error in validate(data)))

    def test_malformed_provider_is_reported_without_crashing(self):
        data = evidence()
        data["models"][0]["provider"] = []
        self.assertIn("provider set is incomplete or unexpected", validate(data))


if __name__ == "__main__":
    unittest.main()
