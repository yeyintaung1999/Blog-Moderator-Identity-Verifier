
from app.moderation_engine import ModerationEngine


def main():
    engine = ModerationEngine()

    content = """
    This article explains the history of illegal drugs,
    their effects on society, and the importance of education
    and prevention.
    """

    assessment = engine.analyze_text(content)

    print(assessment.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
