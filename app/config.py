import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")

BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "jp.anthropic.claude-opus-4-8"
)