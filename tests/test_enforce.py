import unittest

from tools.enforce import (
    EnforcementError,
    ModelRequest,
    build_system_instruction,
    enforce,
    lossless_reflow_signal,
    resolve_mode,
)


PROTOCOL = "Use 6X6. Target six lines and six words."


class EnforceTests(unittest.TestCase):
    def test_first_compliant_signal_is_released(self):
        calls = []

        def invoke(request: ModelRequest):
            calls.append(request)
            return "Ship after tests pass."

        result = enforce(invoke, "Should I ship?", protocol=PROTOCOL)
        self.assertEqual(result.output, "Ship after tests pass.")
        self.assertEqual(result.response_mode, "signal")
        self.assertEqual(len(result.attempts), 1)
        self.assertTrue(calls[0].system_instruction.startswith(PROTOCOL))
        self.assertIn("HOST ENFORCEMENT CONTRACT", calls[0].system_instruction)
        self.assertEqual(calls[0].user_content, "Should I ship?")
        self.assertEqual(calls[0].attempt, 1)
        self.assertIsNone(calls[0].repair_instruction)

    def test_host_contract_can_be_disabled(self):
        requests = []
        enforce(
            lambda request: requests.append(request) or "Short answer.",
            "Answer",
            protocol=PROTOCOL,
            host_contract=False,
        )
        self.assertEqual(requests[0].system_instruction, PROTOCOL)

    def test_build_system_instruction_rejects_empty_protocol(self):
        with self.assertRaises(ValueError):
            build_system_instruction("   ")

    def test_noncompliant_signal_is_repaired(self):
        outputs = [
            "This line deliberately contains far more than six words and should fail structural validation.",
            "Do not ship yet.\nTests still fail.",
        ]
        requests = []

        def invoke(request: ModelRequest):
            requests.append(request)
            return outputs.pop(0)

        result = enforce(invoke, "Should I ship?", protocol=PROTOCOL, max_retries=1)
        self.assertEqual(len(result.attempts), 2)
        self.assertIn("Repair the prior answer", requests[1].repair_instruction)
        self.assertIn("six non-protected", requests[1].repair_instruction)
        self.assertEqual(requests[1].prior_output, result.attempts[0].output)
        self.assertTrue(result.attempts[-1].structural.compliant)

    def test_empty_response_is_retried(self):
        outputs = ["", "Recovered answer."]
        requests = []

        def invoke(request: ModelRequest):
            requests.append(request)
            return outputs.pop(0)

        result = enforce(invoke, "Answer", protocol=PROTOCOL, max_retries=1)
        self.assertEqual(result.output, "Recovered answer.")
        self.assertEqual(len(result.attempts), 2)
        self.assertFalse(result.attempts[0].nonempty)
        self.assertIn("prior response was empty", requests[1].repair_instruction)

    def test_repeated_empty_response_fails_closed(self):
        with self.assertRaises(EnforcementError):
            enforce(lambda _request: "", "Answer", protocol=PROTOCOL, max_retries=1)

    def test_non_text_response_is_retryable(self):
        outputs = [None, "Recovered."]

        def invoke(_request):
            return outputs.pop(0)

        result = enforce(invoke, "Answer", protocol=PROTOCOL, max_retries=1)
        self.assertEqual(result.output, "Recovered.")
        self.assertEqual(len(result.attempts), 2)

    def test_fail_closed_blocks_noncompliant_signal(self):
        def invoke(_request: ModelRequest):
            return "This response keeps violating the six word target on purpose every single time."

        with self.assertRaises(EnforcementError):
            enforce(invoke, "Answer", protocol=PROTOCOL, max_retries=1)

    def test_semantic_validator_can_force_retry(self):
        outputs = ["Tests pass.", "Do not merge.\nTests still fail."]

        def invoke(_request: ModelRequest):
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

    def test_lossless_reflow_preserves_tokens(self):
        original = "one two three four five six seven eight nine ten"
        reflowed = lossless_reflow_signal(original)
        self.assertEqual(reflowed.split(), original.split())
        self.assertEqual(reflowed, "one two three four five six\nseven eight nine ten")

    def test_lossless_reflow_rejects_more_than_36_tokens(self):
        self.assertIsNone(lossless_reflow_signal(" ".join(["word"] * 37)))

    def test_lossless_reflow_can_release_structural_failure(self):
        text = "one two three four five six seven eight nine ten"
        result = enforce(
            lambda _request: text,
            "Answer",
            protocol=PROTOCOL,
            max_retries=0,
            allow_lossless_reflow=True,
        )
        self.assertTrue(result.attempts[0].reflowed)
        self.assertTrue(result.attempts[0].structural.compliant)
        self.assertEqual(result.output.split(), text.split())

    def test_lossless_reflow_disabled_by_default(self):
        text = "one two three four five six seven eight nine ten"
        with self.assertRaises(EnforcementError):
            enforce(lambda _request: text, "Answer", protocol=PROTOCOL, max_retries=0)

    def test_lossless_reflow_skipped_when_protected_layout_exists(self):
        text = "one two three four five six seven eight nine ten"
        with self.assertRaises(EnforcementError):
            enforce(
                lambda _request: text,
                "Answer",
                protocol=PROTOCOL,
                max_retries=0,
                allow_lossless_reflow=True,
                protected_lines={2},
            )

    def test_full_is_not_forced_through_signal_size_gate(self):
        long_full = " ".join(["detailed"] * 80)
        requests = []

        def invoke(request: ModelRequest):
            requests.append(request)
            return long_full

        result = enforce(invoke, "Full explanation, please.", protocol=PROTOCOL)
        self.assertEqual(result.response_mode, "full")
        self.assertEqual(result.output, long_full)
        self.assertEqual(len(result.attempts), 1)
        self.assertIsNone(result.attempts[0].structural)
        self.assertEqual(requests[0].response_mode, "full")

    def test_expand_is_not_forced_through_signal_size_gate(self):
        long_expand = "This expansion intentionally contains many words because the Signal size target must not constrain expansion."
        result = enforce(lambda _request: long_expand, "Expand line 2.", protocol=PROTOCOL)
        self.assertEqual(result.response_mode, "expand")
        self.assertIsNone(result.attempts[0].structural)

    def test_full_semantic_failure_retries_without_signal_constraint(self):
        outputs = ["Incomplete detail.", "Complete detailed answer with all requested facts and supporting explanation."]
        requests = []

        def invoke(request: ModelRequest):
            requests.append(request)
            return outputs.pop(0)

        result = enforce(
            invoke,
            "Full answer.",
            protocol=PROTOCOL,
            max_retries=1,
            semantic_validator=lambda text: text.startswith("Complete"),
        )
        self.assertEqual(len(result.attempts), 2)
        self.assertIn("do not force it into the Signal", requests[1].repair_instruction)
        self.assertIsNone(result.attempts[-1].structural)

    def test_explicit_mode_overrides_auto_detection(self):
        result = enforce(
            lambda _request: "Short answer.",
            "Explain this.",
            protocol=PROTOCOL,
            response_mode="signal",
        )
        self.assertEqual(result.response_mode, "signal")
        self.assertIsNotNone(result.attempts[0].structural)

    def test_single_prompt_fallback_is_explicitly_renderable(self):
        request = ModelRequest(
            system_instruction="SYSTEM",
            user_content="USER",
            response_mode="signal",
            attempt=1,
        )
        rendered = request.as_single_prompt()
        self.assertIn("SYSTEM", rendered)
        self.assertIn("USER", rendered)
        self.assertIn("<6x6_system_instruction>", rendered)

    def test_mode_resolution(self):
        self.assertEqual(resolve_mode("Answer normally", "auto"), "signal")
        self.assertEqual(resolve_mode("Expand line 2", "auto"), "expand")
        self.assertEqual(resolve_mode("Give me the full explanation", "auto"), "full")

    def test_empty_prompt_is_rejected(self):
        with self.assertRaises(ValueError):
            enforce(lambda _: "ok", "   ", protocol=PROTOCOL)


if __name__ == "__main__":
    unittest.main()
