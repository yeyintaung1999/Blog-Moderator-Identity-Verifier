
from app.document.document_detection_engine import DocumentDetectionEngine
from app.document.schemas import DocumentExtractionResult
from app.s3_image_loader import S3ImageLoader


class DocumentExtractionService:
    def __init__(self):
        self.image_loader = S3ImageLoader()
        self.detection_engine = DocumentDetectionEngine()

    def extract(
        self,
        bucket: str,
        front_image_key: str,
        back_image_key: str,
    ) -> DocumentExtractionResult:

        front_image = self.image_loader.load_image(
            bucket=bucket,
            key=front_image_key,
        )

        back_image = self.image_loader.load_image(
            bucket=bucket,
            key=back_image_key,
        )

        return self.detection_engine.extract(
            front_image=front_image,
            back_image=back_image,
        )
