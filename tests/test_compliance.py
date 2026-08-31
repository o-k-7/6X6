import unittest

from tools.check_6x6 import check_signal, count_words


class WordCountingTests(unittest.TestCase):
    def test_blank_line_has_zero_words(self):
        self.assertEqual(count_words("   "), 0)

    def test_words_are_whitespace_separated(self):
        self.assertEqual(count_words("Six words are easy to count"), 6)


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
        self.assertEqual(result.violating_lines, ())

    def test_more_than_six_content_lines_fails(self):
        text = "\n".join(f"Line {number}" for number in range(1, 8))
        result = check_signal(text)
        self.assertFalse(result.compliant)
        self.assertEqual(result.content_lines, 7)

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

    def test_protected_line_can_exceed_word_limit(self):
        text = "Run this exact command:\npython tools/check_6x6.py examples/sample-signal.txt --protect 2"
        result = check_signal(text, protected_lines={2})
        self.assertTrue(result.compliant)
        self.assertEqual(result.violating_lines, ())

    def test_protected_line_still_counts_toward_line_limit(self):
        text = "\n".join(f"protected line number {number}" for number in range(1, 8))
        result = check_signal(text, protected_lines=set(range(1, 8)))
        self.assertFalse(result.compliant)
        self.assertEqual(result.content_lines, 7)


if __name__ == "__main__":
    unittest.main()
