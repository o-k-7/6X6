import unittest

from tools.enforce import EnforcementError, enforce


PROTOCOL = "Use 6X6. Target six lines and six words."


class EnforceTests(unittest.TestCase):
    def test_first_compliant_output_is_released(self):
        calls = []

        def invoke(prompt):
            calls.append(prompt)
            return "Ship after tests pass."

        result = enforce(invoke, "Should I ship?", protocol=PROTOCOL)
        self.assertEqual(result.output, "Ship after tests pass.")
        self.assertEqual(len(result.attempts), 1)
        self.assertIn("<6x6_protocol>", calls[0])
        self.assertIn("Should I ship?", calls[0])

    def test_noncompliant_output_is_repaired(self):
        outputs = [
            "This line deliberately contains far more than six words and should fail structural validation.",
            "Do not ship yet.\nTests still fail.",
        ]
        prompts = []

        def invoke(prompt):
            prompts.append(prompt)
            return outputs.pop(0)

        result = enforce(invoke, "Should I ship?", protocol=PROTOCOL, max_retries=1)
        self.assertEqual(len(result.attempts), 2)
        self.assertIn("Repair the prior answer", prompts[1])
        self.assertTrue(result.attempts[-1].structural.compliant)

    def test_fail_closed_blocks_noncompliant_output(self):
        def invoke(_prompt):
            return "This response keeps violating the six word target on purpose every single time."

        with self.assertRaises(EnforcementError):
            enforce(invoke, "Answer", protocol=PROTOCOL, max_retries=1)

    def test_semantic_validator_can_force_retry(self):
        outputs = ["Tests pass.", "Do not merge.\nTests still fail."]

        def invoke(_prompt):
            return outputs.pop(0)

        result = enforce(
            invoke,
            "Two tests fail. Can I merge?",
            protocol=PROTOCOL,
            max_retries=1,
            semantic_validator=lambda text: "Do not merge" in text,
        )
        self.assertEqual(len(result.attempts), 2)
        self.assertIn("Do not merge", result.output)

    def test_empty_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            enforce(lambda _: "ok", "   ", protocol=PROTOCOL)


if __name__ == "__main__":
    unittest.main()
