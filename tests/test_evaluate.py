import unittest

from tools.evaluate import critical_term_recall, evaluate, evaluate_case


class CriticalTermRecallTests(unittest.TestCase):
    def test_all_terms_found(self):
        recall, found, missing = critical_term_recall("Back up and verify now", ["back up", "verify"])
        self.assertEqual(recall, 1.0)
        self.assertEqual(found, ("back up", "verify"))
        self.assertEqual(missing, ())

    def test_recall_is_case_insensitive(self):
        recall, _, missing = critical_term_recall("NOT YET", ["not yet"])
        self.assertEqual(recall, 1.0)
        self.assertEqual(missing, ())

    def test_missing_term_reduces_recall(self):
        recall, found, missing = critical_term_recall("Backup first", ["backup", "verify"])
        self.assertEqual(recall, 0.5)
        self.assertEqual(found, ("backup",))
        self.assertEqual(missing, ("verify",))


class EvaluationTests(unittest.TestCase):
    def test_case_scores_structure_and_retention(self):
        case = {"id": "x", "critical_terms": ["tests", "failing"]}
        output = {"id": "x", "signal": "Two tests are failing."}
        score = evaluate_case(case, output)
        self.assertTrue(score.compliant)
        self.assertEqual(score.critical_term_recall, 1.0)

    def test_unknown_case_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([{"id": "known", "critical_terms": []}], [{"id": "unknown", "signal": "Hello"}])

    def test_empty_outputs_are_supported(self):
        report = evaluate([], [])
        self.assertEqual(report["cases"], 0)
        self.assertEqual(report["compliance_rate"], 0.0)
        self.assertEqual(report["mean_critical_term_recall"], 0.0)


if __name__ == "__main__":
    unittest.main()
