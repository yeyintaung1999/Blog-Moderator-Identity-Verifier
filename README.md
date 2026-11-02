# Blog Moderator

Blog Moderator is a Python tool for checking blog posts and images for inappropriate content. It also supports extracting information from Japanese identity documents.

It uses Amazon Bedrock for AI analysis and Amazon S3 to retrieve images.

## Features

- Detects hate speech, violence, adult content, drugs, and illegal content in text and images.
- Scores moderation results and decides whether content should be approved, reviewed, or rejected.
- Recognizes Japanese residence cards, My Number cards, and driver's licenses.
- Extracts information from the front and back of identity documents.
- Supports retrieving images directly from Amazon S3.

## Requirements

- Python 3.10+
- AWS credentials with Amazon Bedrock access
- An S3 bucket with permission to read image files

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure your AWS settings in a `.env` file:

```dotenv
AWS_REGION=ap-northeast-1
BEDROCK_MODEL_ID=jp.anthropic.claude-opus-4-8
```

Make sure the selected Bedrock model is available in your AWS account and region.

## Usage

### 1. Text Moderation

```python
from app.moderation_engine import ModerationEngine

engine = ModerationEngine()
result = engine.analyze_text("Your blog post text")

print(result.model_dump_json(indent=2))
```

### 2. Text and Image Moderation

```python
from app.moderation_service import ModerationService

result = ModerationService().moderate(
    blog_id="BLOG-001",
    content="Your blog post text",
    images=[
        {
            "bytes": image_bytes,
            "content_type": "image/jpeg",
            "size": len(image_bytes)
        }
    ],
)

print(result.model_dump_json(indent=2))
```

The moderation service combines AI analysis with a scoring system:

- Below 0.30: Approved
- 0.30–0.69: Manual review
- 0.70 and above: Rejected

### 3. Japanese ID Document Extraction

The document extraction service retrieves front and back images from S3 and extracts their information.

```python
from app.document.document_extraction_service import DocumentExtractionService

result = DocumentExtractionService().extract(
    bucket="your-s3-bucket",
    front_image_key="documents/front.jpg",
    back_image_key="documents/back.jpg",
)

print(result.model_dump_json(indent=2))
```

Supported documents include residence cards, My Number cards, and Japanese driver's licenses.

## Example Scripts

You can run the example scripts directly:

```bash
python -m app.test_moderation
python -m app.test_scoring
```

Some examples require S3 bucket names and image keys to be configured in your environment. Live AWS requests may incur charges.

## Project Structure

```text
app/
├── config.py
├── moderation_engine.py
├── moderation_service.py
├── scoring_engine.py
├── s3_image_loader.py
├── schemas.py
└── document/
    ├── document_detection_engine.py
    ├── document_extraction_service.py
    └── schemas.py
```

**Note:** This project currently provides Python modules and example scripts. It does not include a web application or HTTP API. Keep AWS credentials and identity document images private.