import boto3

from app.config import AWS_REGION


class S3ImageLoader:

    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION
        )

    def load_image(self, bucket: str, key: str) -> dict:

        response = self.client.get_object(
            Bucket=bucket,
            Key=key
        )

        image_bytes = response["Body"].read()

        return {
            "bytes": image_bytes,
            "content_type": response.get("ContentType"),
            "size": len(image_bytes),
        }