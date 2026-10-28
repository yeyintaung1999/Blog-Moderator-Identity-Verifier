
from app.schemas import (
    BlogModerationAssessment,
    CategoryAssessment,
    ModerationCategory,
)
from app.scoring_engine import ScoringEngine


def main():

    assessment = BlogModerationAssessment(
        categories={
            ModerationCategory.HATE_SPEECH: CategoryAssessment(
                present=True,
                policy_violation=True,
                confidence=0.95,
                severity=0.90,
                reason="Targeted hateful language",
                evidence=["Example hateful statement"],
            ),

            ModerationCategory.VIOLENCE: CategoryAssessment(
                present=True,
                policy_violation=True,
                confidence=0.90,
                severity=0.40,
                reason="Non-graphic violent discussion",
                evidence=["Example violent statement"],
            ),

            ModerationCategory.ADULT_CONTENT: CategoryAssessment(
                present=False,
                policy_violation=False,
                confidence=0.99,
                severity=0.0,
                reason="No adult content",
                evidence=[],
            ),

            ModerationCategory.PORNOGRAPHY: CategoryAssessment(
                present=False,
                policy_violation=False,
                confidence=0.99,
                severity=0.0,
                reason="No pornography",
                evidence=[],
            ),

            ModerationCategory.DRUGS: CategoryAssessment(
                present=True,
                policy_violation=False,
                confidence=0.97,
                severity=0.0,
                reason="Educational discussion",
                evidence=["Educational article about drugs"],
            ),

            ModerationCategory.ILLEGAL_CONTENT: CategoryAssessment(
                present=False,
                policy_violation=False,
                confidence=0.97,
                severity=0.0,
                reason="No illegal activity promoted",
                evidence=[],
            ),
        }
    )

    engine = ScoringEngine()

    score = engine.calculate_score(assessment)
    decision = engine.make_decision(score)

    print("Score:", score)
    print("Decision:", decision.value)


if __name__ == "__main__":
    main()
