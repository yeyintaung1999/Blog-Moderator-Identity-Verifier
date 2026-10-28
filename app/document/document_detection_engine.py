
import json
import re
from typing import Any

import boto3
from pydantic import TypeAdapter, ValidationError

from app.config import AWS_REGION, BEDROCK_MODEL_ID
from app.document.prompts import DOCUMENT_EXTRACTION_PROMPT
from app.document.schemas import DocumentExtractionResult


class DocumentDetectionEngine:
    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )

        self.document_adapter = TypeAdapter(DocumentExtractionResult)

    def extract(
        self,
        front_image: dict[str, Any],
        back_image: dict[str, Any],
    ) -> DocumentExtractionResult:

        message_content: list[dict[str, Any]] = [
            {
                "text": (
                    "Identify the Japanese identity document and extract "
                    "its information.\n\n"
                    "The first image is the FRONT side.\n"
                    "The second image is the BACK side.\n\n"
                    "Analyze both images together, but keep their extracted "
                    "fields separated by side."
                )
            }
        ]

        images = [
            ("FRONT", front_image),
            ("BACK", back_image),
        ]

        for side, image in images:
            content_type = image.get("content_type")

            image_format = {
                "image/jpeg": "jpeg",
                "image/jpg": "jpeg",
                "image/png": "png",
                "image/gif": "gif",
                "image/webp": "webp",
                "image/jxl": "jpeg"
            }.get((content_type or "").lower())

            if image_format is None:
                raise ValueError(
                    f"Unsupported {side} image content type: {content_type}"
                )

            message_content.append({
                "text": f"{side} DOCUMENT IMAGE:"
            })

            message_content.append({
                "image": {
                    "format": image_format,
                    "source": {
                        "bytes": image["bytes"]
                    },
                }
            })

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            system=[
                {"text": DOCUMENT_EXTRACTION_PROMPT}
            ],
            messages=[
                {
                    "role": "user",
                    "content": message_content,
                }
            ],
            inferenceConfig={
                "maxTokens": 3000,
                "temperature": 0,
            },
        )

        response_text = "".join(
            block["text"]
            for block in response["output"]["message"]["content"]
            if "text" in block
        ).strip()

        response_text = re.sub(
            r"^```(?:json)?\s*",
            "",
            response_text,
        )
        response_text = re.sub(
            r"\s*```$",
            "",
            response_text,
        )

        try:
            result = json.loads(response_text)

            return self.document_adapter.validate_python(result)

        except (json.JSONDecodeError, ValidationError) as error:
            raise ValueError(
                f"Invalid document extraction response: {error}\n"
                f"Raw response: {response_text}"
            ) from error
