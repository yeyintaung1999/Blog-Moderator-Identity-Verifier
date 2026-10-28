
import json
import re

import boto3
from pydantic import ValidationError

from app.config import AWS_REGION, BEDROCK_MODEL_ID
from app.prompts import MODERATION_SYSTEM_PROMPT
from app.schemas import BlogModerationAssessment


class ModerationEngine:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION
        )

    def analyze_text(self, content: str) -> BlogModerationAssessment:

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            system=[
                {"text": MODERATION_SYSTEM_PROMPT}
            ],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": (
                                "Analyze the following blog content. "
                                "Return only the moderation assessment "
                                "as valid JSON.\n\n"
                                f"<blog_content>\n{content}\n</blog_content>"
                            )
                        }
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": 2000,
                "temperature": 0
            }
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        # Remove Markdown code fences if the model still includes them.
        response_text = response_text.strip()
        response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
        response_text = re.sub(r"\s*```$", "", response_text)

        try:
            result = json.loads(response_text)

            return BlogModerationAssessment.model_validate(result)

        except (json.JSONDecodeError, ValidationError) as error:
            raise ValueError(
                f"Invalid moderation response: {error}\n"
                f"Raw response: {response_text}"
            ) from error

    
    def analyze_multimodal(
        self,
        content: str,
        images: list[dict],
    ) -> BlogModerationAssessment:

        # First content block: blog text
        from typing import Any

        message_content: list[dict[str, Any]] = [
            {
                "text": (
                    "Analyze this blog content and all attached images. "
                    "Evaluate them together, considering their context.\n\n"
                    f"<blog_content>\n{content}\n</blog_content>"
                )
            }
        ]

        # Add image content blocks
        for image in images:

            content_type = image["content_type"]

            image_format = {
                "image/jpeg": "jpeg",
                "image/jpg": "jpeg",
                "image/png": "png",
                "image/gif": "gif",
                "image/webp": "webp",
            }.get(content_type.lower())

            if image_format is None:
                raise ValueError(
                    f"Unsupported image content type: {content_type}"
                )

            message_content.append({
                "image": {
                    "format": image_format,
                    "source": {
                        "bytes": image["bytes"]
                    }
                }
            })

        response = self.client.converse(
            modelId=BEDROCK_MODEL_ID,
            system=[
                {"text": MODERATION_SYSTEM_PROMPT}
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

        response_text = response["output"]["message"]["content"][0]["text"]

        response_text = response_text.strip()
        response_text = re.sub(r"^```(?:json)?\s*", "", response_text)
        response_text = re.sub(r"\s*```$", "", response_text)

        try:
            result = json.loads(response_text)

            return BlogModerationAssessment.model_validate(result)

        except (json.JSONDecodeError, ValidationError) as error:
            raise ValueError(
                f"Invalid moderation response: {error}\n"
                f"Raw response: {response_text}"
            ) from error

