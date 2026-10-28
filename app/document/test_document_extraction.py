
import os

from dotenv import load_dotenv

from app.document.document_extraction_service import (
    DocumentExtractionService,
)

load_dotenv()


def main():
    service = DocumentExtractionService()

    test_documents = [
        {
            "name": "RESIDENCE_CARD",
            "front_key": os.environ["RESIDENCE_CARD_FRONT_KEY"],
            "back_key": os.environ["RESIDENCE_CARD_BACK_KEY"],
        },
        # {
        #     "name": "MY_NUMBER_CARD",
        #     "front_key": os.environ["MY_NUMBER_CARD_FRONT_KEY"],
        #     "back_key": os.environ["MY_NUMBER_CARD_BACK_KEY"],
        # },
        # {
        #     "name": "DRIVER_LICENSE",
        #     "front_key": os.environ["DRIVER_LICENSE_FRONT_KEY"],
        #     "back_key": os.environ["DRIVER_LICENSE_BACK_KEY"],
        # },
    ]

    bucket = os.environ["S3_BUCKET"]

    for document in test_documents:
        print(f"\n========== {document['name']} ==========")

        try:
            result = service.extract(
                bucket=bucket,
                front_image_key=document["front_key"],
                back_image_key=document["back_key"],
            )

            print(result.model_dump_json(indent=2))

        except Exception as error:
            print(f"Extraction failed: {error}")


if __name__ == "__main__":
    main()
