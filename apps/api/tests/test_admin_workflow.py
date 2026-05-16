import unittest

from app.admin_workflow import (
    PUBLISHED_INCIDENTS,
    create_incident_from_task,
    find_review_task,
    update_review_task,
)
from app.models import IncidentCreateRequest, ReviewUpdateRequest


class AdminWorkflowTest(unittest.TestCase):
    def tearDown(self) -> None:
        PUBLISHED_INCIDENTS.clear()
        task = find_review_task("task-001")
        if task is not None:
            task.review_status = "pending"
            task.reviewer_notes = ""

    def test_reviewer_can_update_status_and_notes(self) -> None:
        updated = update_review_task(
            "task-001",
            ReviewUpdateRequest(
                review_status="needs_more_evidence",
                reviewer_notes="Need county election office confirmation.",
                suggested_risk_level="critical",
            ),
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated.review_status, "needs_more_evidence")
        self.assertEqual(updated.suggested_risk_level, "critical")
        self.assertIn("county election office", updated.reviewer_notes)

    def test_publish_task_creates_public_incident(self) -> None:
        update_review_task(
            "task-001",
            ReviewUpdateRequest(review_status="approved", reviewer_notes="Ready for publication."),
        )
        incident = create_incident_from_task(IncidentCreateRequest(task_id="task-001"))

        self.assertIsNotNone(incident)
        self.assertEqual(incident.id, "review-task-001")
        self.assertEqual(find_review_task("task-001").review_status, "published")
        self.assertEqual(len(PUBLISHED_INCIDENTS), 1)


if __name__ == "__main__":
    unittest.main()
