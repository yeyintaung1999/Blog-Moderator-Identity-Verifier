
import os

from dotenv import load_dotenv

from app.moderation_engine import ModerationEngine
from app.s3_image_loader import S3ImageLoader

load_dotenv()


def main():

    loader = S3ImageLoader()
    engine = ModerationEngine()

    # Load image from S3
    image1 = loader.load_image(
        bucket=os.environ["S3_BUCKET"],
        key=os.environ["S3_IMAGE_KEY1"],
    )
    image2 = loader.load_image(
            bucket=os.environ["S3_BUCKET"],
            key=os.environ["S3_IMAGE_KEY2"],
        )
    image3 = loader.load_image(
                bucket=os.environ["S3_BUCKET"],
                key=os.environ["S3_IMAGE_KEY3"],
            )
    image4 = loader.load_image(
                    bucket=os.environ["S3_BUCKET"],
                    key=os.environ["S3_IMAGE_KEY4"],
                )
    # Analyze text and image together
    assessment = engine.analyze_multimodal(
        content="""
        Please review this blog post about the attached image.
        """,
        images=[image1, image2, image3, image4],
    )

    print(assessment.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
