
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    RESIDENCE_CARD = "RESIDENCE_CARD"
    MY_NUMBER_CARD = "MY_NUMBER_CARD"
    DRIVER_LICENSE = "DRIVER_LICENSE"


class ResidenceCardFields(BaseModel):
    full_name: str | None = None
    date_of_birth: str | None = None
    nationality: str | None = None
    address: str | None = None
    residence_status: str | None = None
    period_of_stay: str | None = None
    expiration_date: str | None = None
    residence_card_number: str | None = None
    work_restrictions: str | None = None


class MyNumberCardFields(BaseModel):
    full_name: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    gender: str | None = None
    expiration_date: str | None = None


class DriverLicenseFields(BaseModel):
    full_name: str | None = None
    date_of_birth: str | None = None
    address: str | None = None
    license_number: str | None = None
    license_type: str | None = None
    issue_date: str | None = None
    expiration_date: str | None = None
    conditions: str | None = None


class ResidenceCardExtraction(BaseModel):
    document_type: Literal[DocumentType.RESIDENCE_CARD]
    front: ResidenceCardFields | None = None
    back: ResidenceCardFields | None = None


class MyNumberCardExtraction(BaseModel):
    document_type: Literal[DocumentType.MY_NUMBER_CARD]
    front: MyNumberCardFields | None = None
    back: MyNumberCardFields | None = None


class DriverLicenseExtraction(BaseModel):
    document_type: Literal[DocumentType.DRIVER_LICENSE]
    front: DriverLicenseFields | None = None
    back: DriverLicenseFields | None = None


DocumentExtraction = Annotated[
    ResidenceCardExtraction
    | MyNumberCardExtraction
    | DriverLicenseExtraction,
    Field(discriminator="document_type"),
]


class DocumentExtractionResult(BaseModel):
    document: DocumentExtraction
    confidence: float = Field(ge=0, le=1)
    missing_fields: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
