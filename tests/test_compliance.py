import unittest

from tools.check_6x6 import _parse_protected_lines, check_signal, count_words


class WordCountingTests(unittest.TestCase):
    def test_blank_line_has_zero_words(self):
        self.assertEqual(count_words("   "), 0)

    def test_words_are_whitespace_separated(self):
        self.assertEqual(count_words("Six words are easy to count"), 6)

    def test_unicode_words_are_supported(self):
        self.assertEqual(count_words("תשובה קצרה וברורה עובדת גם בעברית"), 6)


class SignalComplianceTests(unittest.TestCase):
    def test_valid_six_by_six_signal_passes(self):
        text = """Ship the fix today.
Tests are green.
No migration is required.
Risk remains low.
Document the behavior change.
Then merge the pull request."""
        result = check_signal(text)
        self.assertTrue(result.compliant)
        self.assertEqual(result.content_lines, 6)
        self.assertEqual(result.target_lines, 6)
        self.assertEqual(result.violating_lines, ())

    def test_more_than_six_target_lines_fails(self):
        text = "\n".join(f"Line {number}" for number in range(1, 8))
        result = check_signal(text)
        self.assertFalse(result.compliant)
        self.assertEqual(result.target_lines, 7)

    def test_more_than_six_words_fails(self):
        text = "This line contains more than six words"
        result = check_signal(text)
        self.assertFalse(result.compliant)
        self.assertEqual(result.violating_lines, (1,))

    def test_blank_lines_do_not_count(self):
        text = "Answer first.\n\nThen take action.\n"
        result = check_signal(text)
        self.assertTrue(result.compliant)
        self.assertEqual(result.content_lines, 2)
        self.assertEqual(result.target_lines, 2)

    def test_protected_line_can_exceed_word_limit(self):
        text = "Run this exact command:\npython tools/check_6x6.py examples/sample-signal.txt --protect 2"
        result = check_signal(text, protected_lines={2})
        self.assertTrue(result.compliant)
        self.assertEqual(result.protected_lines, (2,))
        self.assertEqual(result.violating_lines, ())

    def test_protected_lines_can_exceed_line_target(self):
        prose = [f"Step {number}" for number in range(1, 7)]
        code = [f"protected exact command number {number} with extra words" for number in range(7, 10)]
        text = "\n".join(prose + code)
        result = check_signal(text, protected_lines={7, 8, 9})
        self.assertTrue(result.compliant)
        self.assertEqual(result.content_lines, 9)
        self.assertEqual(result.target_lines, 6)

    def test_one_protected_line_leaves_six_target_lines(self):
        text = "\n".join(f"Line {number}" for number in range(1, 8))
        result = check_signal(text, protected_lines={1})
        self.assertTrue(result.compliant)
        self.assertEqual(result.target_lines, 6)

    def test_nonexistent_protected_line_is_ignored(self):
        result = check_signal("One line.", protected_lines={99})
        self.assertEqual(result.protected_lines, ())
        self.assertEqual(result.target_lines, 1)


class ProtectedLineParsingTests(unittest.TestCase):
    def test_parse_protected_lines(self):
        self.assertEqual(_parse_protected_lines("2, 4,4"), {2, 4})

    def test_zero_line_rejected(self):
        with self.assertRaises(ValueError):
            _parse_protected_lines("0")


if __name__ == "__main__":
    unittest.main()
