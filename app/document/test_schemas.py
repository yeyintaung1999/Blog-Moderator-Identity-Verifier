
from app.document.schemas import (
    DocumentExtractionResult,
    DocumentType,
    DriverLicenseExtraction,
    DriverLicenseFields,
    MyNumberCardExtraction,
    MyNumberCardFields,
    ResidenceCardExtraction,
    ResidenceCardFields,
)


def test_residence_card():
    return ResidenceCardExtraction(
        document_type=DocumentType.RESIDENCE_CARD,
        front=ResidenceCardFields(
            full_name="TEST USER",
            date_of_birth="1995-01-01",
            nationality="MYANMAR",
            residence_status="ENGINEER",
        ),
        back=ResidenceCardFields(
            address="TOKYO",
            residence_card_number="TEST-123456",
        ),
    )


def test_my_number_card():
    return MyNumberCardExtraction(
        document_type=DocumentType.MY_NUMBER_CARD,
        front=MyNumberCardFields(
            full_name="TEST USER",
            date_of_birth="1995-01-01",
            address="TOKYO",
            gender="MALE",
        ),
        back=MyNumberCardFields(),
    )


def test_driver_license():
    return DriverLicenseExtraction(
        document_type=DocumentType.DRIVER_LICENSE,
        front=DriverLicenseFields(
            full_name="TEST USER",
            date_of_birth="1995-01-01",
            address="TOKYO",
            license_number="TEST-123456",
            license_type="普通",
        ),
        back=DriverLicenseFields(
            conditions="眼鏡等",
        ),
    )


def main():
    test_cases = [
        test_residence_card(),
        test_my_number_card(),
        test_driver_license(),
    ]

    for document in test_cases:
        result = DocumentExtractionResult(
            document=document,
            confidence=0.95,
            missing_fields=[],
            warnings=[],
        )

        print(f"\n===== {document.document_type.value} =====")
        print(result.model_dump_json(indent=2))

    print("\nAll three document schemas validated successfully!")


if __name__ == "__main__":
    main()
