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
        output = {"id": "x", "signal": "Two tests are failing.", "status": "pass"}
        score = evaluate_case(case, output)
        self.assertTrue(score.compliant)
        self.assertEqual(score.critical_term_recall, 1.0)
        self.assertEqual(score.status, "pass")

    def test_unknown_case_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([{"id": "known", "critical_terms": []}], [{"id": "unknown", "signal": "Hello"}])

    def test_missing_output_fails_strict_evaluation(self):
        cases = [{"id": "a", "critical_terms": []}, {"id": "b", "critical_terms": []}]
        with self.assertRaises(ValueError):
            evaluate(cases, [{"id": "a", "signal": "Fine.", "status": "pass"}])

    def test_partial_mode_never_reports_all_passed(self):
        cases = [{"id": "a", "critical_terms": []}, {"id": "b", "critical_terms": []}]
        report = evaluate(cases, [{"id": "a", "signal": "Fine.", "status": "pass"}], require_complete=False)
        self.assertFalse(report["complete"])
        self.assertFalse(report["all_passed"])
        self.assertEqual(report["missing_cases"], ["b"])

    def test_blocked_case_is_not_a_pass(self):
        cases = [{"id": "a", "critical_terms": []}]
        report = evaluate(cases, [{"id": "a", "status": "blocked"}])
        self.assertTrue(report["complete"])
        self.assertFalse(report["all_passed"])
        self.assertEqual(report["pass_rate"], 0.0)

    def test_duplicate_output_is_rejected(self):
        cases = [{"id": "a", "critical_terms": []}]
        with self.assertRaises(ValueError):
            evaluate(cases, [{"id": "a", "signal": "One"}, {"id": "a", "signal": "Two"}])


if __name__ == "__main__":
    unittest.main()
