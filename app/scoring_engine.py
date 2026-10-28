
from app.schemas import (
    BlogModerationAssessment,
    ModerationDecision,
)


class ScoringEngine:

    APPROVE_THRESHOLD = 0.30
    REJECT_THRESHOLD = 0.70

    def calculate_score(
        self,
        assessment: BlogModerationAssessment,
    ) -> float:

        category_risks = []

        for result in assessment.categories.values():

            if not result.policy_violation:
                continue

            risk = result.confidence * result.severity

            category_risks.append(risk)

        if not category_risks:
            return 0.0

        return round(max(category_risks), 4)

    def make_decision(
        self,
        score: float,
    ) -> ModerationDecision:

        if score < self.APPROVE_THRESHOLD:
            return ModerationDecision.APPROVE

        if score < self.REJECT_THRESHOLD:
            return ModerationDecision.MANUAL_REVIEW

        return ModerationDecision.REJECT

