import unittest

from tools.live_acceptance import REQUIRED_PROVIDERS, REQUIRED_SCENARIOS, validate


def complete_model(provider: str) -> dict:
    scenarios = []
    for scenario_id in REQUIRED_SCENARIOS:
        item = {
            "id": scenario_id,
            "status": "pass",
            "input": "synthetic input",
            "output_6x6": "Compact output.",
            "retries": 0,
        }
        if scenario_id == "baseline_be_concise":
            item["output_baseline"] = "Baseline output."
        scenarios.append(item)
    return {
        "provider": provider,
        "model_id": f"{provider}-model",
        "model_version": "snapshot",
        "date": "2026-09-07",
        "runtime": "test-runtime",
        "prompt_sha256": "0" * 64,
        "activation": "persistent",
        "scenarios": scenarios,
    }


class LiveAcceptanceTests(unittest.TestCase):
    def complete_data(self):
        return {"models": [complete_model(provider) for provider in REQUIRED_PROVIDERS]}

    def test_complete_matrix_passes(self):
        self.assertEqual(validate(self.complete_data()), [])

    def test_missing_provider_fails(self):
        data = {"models": [complete_model(provider) for provider in REQUIRED_PROVIDERS[:-1]]}
        errors = validate(data)
        self.assertTrue(any("missing providers" in error for error in errors))

    def test_blocked_scenario_fails(self):
        data = self.complete_data()
        data["models"][0]["scenarios"][0]["status"] = "blocked"
        errors = validate(data)
        self.assertTrue(any("status is blocked" in error for error in errors))

    def test_missing_baseline_output_fails(self):
        data = self.complete_data()
        target = next(s for s in data["models"][0]["scenarios"] if s["id"] == "baseline_be_concise")
        target.pop("output_baseline")
        errors = validate(data)
        self.assertTrue(any("missing baseline output" in error for error in errors))

    def test_duplicate_provider_fails(self):
        models = self.complete_data()["models"]
        models.append(complete_model(REQUIRED_PROVIDERS[0]))
        errors = validate({"models": models})
        self.assertIn("duplicate provider records", errors)

    def test_invalid_hash_fails(self):
        data = self.complete_data()
        data["models"][0]["prompt_sha256"] = "not-a-hash"
        errors = validate(data)
        self.assertTrue(any("prompt_sha256" in error for error in errors))

    def test_invalid_activation_fails(self):
        data = self.complete_data()
        data["models"][0]["activation"] = "always_on"
        errors = validate(data)
        self.assertTrue(any("activation must be" in error for error in errors))

    def test_invalid_date_fails(self):
        data = self.complete_data()
        data["models"][0]["date"] = "09/07/2026"
        errors = validate(data)
        self.assertTrue(any("date must be YYYY-MM-DD" in error for error in errors))

    def test_unexpected_scenario_fails(self):
        data = self.complete_data()
        data["models"][0]["scenarios"].append(
            {"id": "made_up", "status": "pass", "input": "x", "output_6x6": "y", "retries": 0}
        )
        errors = validate(data)
        self.assertTrue(any("unexpected scenarios" in error for error in errors))

    def test_boolean_retry_is_rejected(self):
        data = self.complete_data()
        data["models"][0]["scenarios"][0]["retries"] = True
        errors = validate(data)
        self.assertTrue(any("retries must be" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
