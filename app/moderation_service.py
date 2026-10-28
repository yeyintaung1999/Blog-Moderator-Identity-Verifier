from app.moderation_engine import ModerationEngine
from app.schemas import BlogModerationResponse
from app.scoring_engine import ScoringEngine


class ModerationService:
    def __init__(self):
        self.moderation_engine = ModerationEngine()
        self.scoring_engine = ScoringEngine()

    def moderate(
        self,
        blog_id: str,
        content: str,
        images: list[dict] | None = None,
    ) -> BlogModerationResponse:

        assessment = self.moderation_engine.analyze_multimodal(
            content=content,
            images=images or [],
        )

        score = self.scoring_engine.calculate_score(assessment)
        decision = self.scoring_engine.make_decision(score)

        return BlogModerationResponse(
            blog_id=blog_id,
            score=score,
            decision=decision,
            assessment=assessment,
        )