import unittest

from tools.ollama_response import ModelResponseError, final_content, model_identity


class OllamaResponseTests(unittest.TestCase):
    def test_reasoning_only_remains_empty(self):
        content, thinking = final_content({"message": {"content": "", "thinking": "private"}})
        self.assertEqual(content, "")
        self.assertTrue(thinking)

    def test_final_content_is_preserved(self):
        content, thinking = final_content({"message": {"content": "Final answer.", "thinking": "private"}})
        self.assertEqual(content, "Final answer.")
        self.assertTrue(thinking)

    def test_non_text_final_is_rejected(self):
        with self.assertRaises(ModelResponseError):
            final_content({"message": {"content": ["not", "text"]}})

    def test_missing_message_is_rejected(self):
        with self.assertRaises(ModelResponseError):
            final_content({})

    def test_model_identity_records_available_digest(self):
        self.assertEqual(model_identity({"model": "deepseek-r1:1.5b", "digest": "abc"}), ("deepseek-r1:1.5b", "abc"))

    def test_invalid_digest_is_rejected(self):
        with self.assertRaises(ModelResponseError):
            model_identity({"model": "m", "digest": 123})


if __name__ == "__main__":
    unittest.main()
