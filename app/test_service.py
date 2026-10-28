import os

from app.moderation_service import ModerationService
from app.s3_image_loader import S3ImageLoader


def main():

    loader = S3ImageLoader()
    service = ModerationService()

    blog_id = "BLOG-001"

    content = """
    
    """

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

    image5 = loader.load_image(
                            bucket=os.environ["S3_BUCKET"],
                            key=os.environ["S3_IMAGE_KEY5"],
                        )

    image6 = loader.load_image(
                                bucket=os.environ["S3_BUCKET"],
                                key=os.environ["S3_IMAGE_KEY6"],
                            )

    image7 = loader.load_image(
                            bucket=os.environ["S3_BUCKET"],
                            key=os.environ["S3_IMAGE_KEY7"],
                        )

    images = [image1, image2, image3, image4, image5, image6, image7]

    result = service.moderate(
            blog_id=blog_id,
            content=content,
            images=images,
        )

    print("\n========== MODERATION RESULT ==========")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
