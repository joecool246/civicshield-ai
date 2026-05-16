import unittest

from app.bias_audits import get_bias_audit, list_bias_audits


class BiasAuditTest(unittest.TestCase):
    def test_seed_topics_are_present(self) -> None:
        topics = {audit.topic for audit in list_bias_audits()}

        self.assertIn("voter ID laws", topics)
        self.assertIn("immigration", topics)
        self.assertIn("policing", topics)
        self.assertIn("climate policy", topics)
        self.assertIn("candidate comparison", topics)
        self.assertIn("voting advice refusal", topics)
        self.assertIn("ballot measure explanation", topics)

    def test_scores_stay_in_range(self) -> None:
        for audit in list_bias_audits():
            scores = [
                audit.source_balance_score,
                audit.framing_score,
                audit.symmetry_score,
                audit.refusal_consistency_score,
                audit.candidate_neutrality_score,
                audit.uncertainty_transparency_score,
            ]
            self.assertTrue(all(0 <= score <= 100 for score in scores))

    def test_fetch_one_audit(self) -> None:
        audit = get_bias_audit("audit-005")

        self.assertIsNotNone(audit)
        self.assertEqual(audit.topic, "candidate comparison")
        self.assertTrue(audit.voting_advice_flag)
        self.assertEqual(audit.overall_bias_risk, "high")


if __name__ == "__main__":
    unittest.main()
