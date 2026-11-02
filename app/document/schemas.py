
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentType(str, Enum):
    RESIDENCE_CARD = "RESIDENCE_CARD"
    MY_NUMBER_CARD = "MY_NUMBER_CARD"
    DRIVER_LICENSE = "DRIVER_LICENSE"

class DocumentBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

class ResidenceCardFrontFields(DocumentBaseModel):

    full_name: str | None = Field(
        default=None,
        description=(
            "The cardholder's full legal name (氏名) as printed on the front "
            "of the Japanese Residence Card (在留カード). Extract the complete "
            "name exactly as visible, preserving the original spelling, "
            "character order, spaces, Japanese characters, and Latin letters. "
            "Do not translate, transliterate, correct, or infer missing characters."
        )
    )

    date_of_birth: str | None = Field(
        default=None,
        description=(
            "The cardholder's date of birth (生年月日) printed on the front. "
            "Convert the date to the Gregorian calendar and return it strictly "
            "in YYYY-MM-DD format. Correctly interpret Japanese era dates "
            "(和暦), including Showa (昭和), Heisei (平成), and Reiwa (令和). "
            "Do not confuse the date of birth with the card's issue or expiration date. "
            "Return null if any part of the date is missing or unreadable."
        )
    )

    nationality: str | None = Field(
        default=None,
        description=(
            "The cardholder's nationality or region of origin "
            "(国籍・地域) exactly as printed on the front. "
            "Preserve the original text without translating it into another "
            "language. Do not infer nationality from the person's name, "
            "address, or other document information."
        )
    )

    address: str | None = Field(
        default=None,
        description=(
            "The cardholder's registered residential address (住居地) "
            "printed on the front of the card. Extract the complete address, "
            "including prefecture, municipality, town, block numbers, building "
            "names, and room numbers when visible. Preserve Japanese characters, "
            "numbers, and original ordering. Do not translate, normalize, "
            "complete, or infer missing address information. Do not extract "
            "address-change history from the reverse side."
        )
    )

    residence_status: str | None = Field(
        default=None,
        description=(
            "The cardholder's official residence status (在留資格) printed "
            "on the front. Extract the complete status exactly as displayed, "
            "including Japanese punctuation and wording. Examples include "
            "「技術・人文知識・国際業務」, 「留学」, and 「家族滞在」. "
            "Do not confuse residence status with nationality, period of stay, "
            "or permission to engage in activities outside the permitted status."
        )
    )

    period_of_stay: str | None = Field(
        default=None,
        description=(
            "The authorized period of stay (在留期間) printed on the front. "
            "Extract the stated duration exactly, such as 「1年」, 「3年」, "
            "「5年」, or 「6月」. This field represents the duration of the "
            "authorized stay, not the expiration date. Do not calculate or "
            "infer the duration from the dates printed on the card."
        )
    )

    expiration_date: str | None = Field(
        default=None,
        description=(
            "The expiration date of the authorized period of stay "
            "(在留期間満了日) printed on the front. Convert Japanese era dates "
            "to Gregorian dates and return strictly in YYYY-MM-DD format. "
            "This is the date until which the authorized period of stay is valid. "
            "Do not confuse it with the card's issue date, date of birth, "
            "or any other date. Return null if unreadable or not explicitly shown."
        )
    )

    residence_card_number: str | None = Field(
        default=None,
        description=(
            "The unique residence card identification number "
            "(在留カード番号) printed on the front. Extract the complete "
            "alphanumeric sequence exactly as displayed. Preserve uppercase "
            "letters, digits, and their original order. Do not insert, remove, "
            "or substitute characters. Pay particular attention to visually "
            "similar characters such as O and 0, I and 1, and B and 8. "
            "Do not confuse this number with any other printed number."
        )
    )

    work_restrictions: str | None = Field(
        default=None,
        description=(
            "The employment permission or restriction statement "
            "(就労制限の有無) printed on the front. Extract the complete "
            "statement exactly as displayed. Examples include "
            "「就労制限なし」 and 「就労不可」. Preserve the original "
            "Japanese wording. Do not infer employment permission from "
            "the residence status. Do not confuse this field with the "
            "separate permission for activities outside the permitted status "
            "(資格外活動許可), which is recorded on the reverse side."
        )
    )


class ResidenceCardBackFields(DocumentBaseModel):

    address: str | None = Field(
        default=None,
        description="住居地記載欄に記載された住所。記載がなければnull。",
    )
    
    work_restrictions: str | None = Field(
        default=None,
        description="資格外活動許可欄に記載された就労・活動制限。記載がなければnull。",
    )

    address_change_history: str | None = Field(
        default=None,
        description=(
            "Address change information (住居地記載欄) "
            "written by the authorities. Preserve the original Japanese text."
        )
    )

    permission_to_engage_in_activity: str | None = Field(
        default=None,
        description=(
            "Permission for activities outside the permitted status "
            "(資格外活動許可). Extract the exact text, including "
            "any restrictions or conditions."
        )
    )

    other_annotations: str | None = Field(
        default=None,
        description=(
            "Other official annotations, stamps, or remarks "
            "visible on the back of the residence card. "
            "Do not include handwritten or printed information "
            "that belongs to unrelated sections."
        )
    )


class ResidenceCardExtraction(DocumentBaseModel):

    document_type: Literal[DocumentType.RESIDENCE_CARD] = Field(
        description=(
            "Document type. Must always be RESIDENCE_CARD "
            "for a Japanese Residence Card (在留カード)."
        )
    )

    front: ResidenceCardFrontFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the FRONT side "
            "of the Japanese Residence Card. "
            "Extract name, date of birth, nationality, address, "
            "residence status, period of stay, expiration date, "
            "residence card number, and work restrictions only "
            "when visible on the front."
        )
    )

    back: ResidenceCardBackFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the BACK side "
            "of the Japanese Residence Card. "
            "Extract address changes, permission to engage in activities "
            "outside the permitted status, and other annotations "
            "only when visible on the back."
        )
    )



class MyNumberCardFrontFields(DocumentBaseModel):

    full_name: str | None = Field(
        default=None,
        description="Full name (氏名) exactly as printed on the front."
    )

    date_of_birth: str | None = Field(
        default=None,
        description=(
            "Date of birth (生年月日). "
            "Convert Japanese era dates into YYYY-MM-DD format."
        )
    )

    address: str | None = Field(
        default=None,
        description="Registered address (住所) exactly as printed."
    )

    gender: str | None = Field(
        default=None,
        description=(
            "Gender (性別), if visibly printed. "
            "Do not infer from the person's name."
        )
    )

    expiration_date: str | None = Field(
        default=None,
        description=(
            "My Number Card expiration date (有効期限). "
            "Convert to YYYY-MM-DD. "
            "Do not confuse with electronic certificate expiration."
        )
    )

class MyNumberCardBackFields(DocumentBaseModel):

    back_side_present: bool = Field(
        description="Whether the uploaded image shows the back of the card."
    )

    qr_code_present: bool | None = Field(
        default=None,
        description="Whether a QR code is visibly present."
    )

    other_visible_information: str | None = Field(
        default=None,
        description=(
            "Other relevant visible printed information. "
            "Do not extract the individual number (個人番号), "
            "QR code contents, or unrelated sensitive information."
        )
    )

class MyNumberCardExtraction(DocumentBaseModel):

    document_type: Literal[DocumentType.MY_NUMBER_CARD] = Field(
        description="Must be MY_NUMBER_CARD."
    )

    front: MyNumberCardFrontFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the FRONT side "
            "of the Japanese My Number Card."
        )
    )

    back: MyNumberCardBackFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the BACK side. "
            "Never extract the individual number."
        )
    )

class DriverLicenseFrontFields(DocumentBaseModel):

    full_name: str | None = Field(
        default=None,
        description="Full name (氏名) exactly as printed."
    )

    date_of_birth: str | None = Field(
        default=None,
        description=(
            "Date of birth (生年月日). "
            "Convert Japanese era dates into YYYY-MM-DD format."
        )
    )

    address: str | None = Field(
        default=None,
        description="Registered address (住所) exactly as printed."
    )

    license_number: str | None = Field(
        default=None,
        description=(
            "Driver's license number (免許証番号). "
            "Preserve every character and leading zero."
        )
    )

    license_type: str | None = Field(
        default=None,
        description=(
            "License categories (種類) currently indicated on the card. "
            "Extract all applicable categories, not just the first."
        )
    )

    issue_date: str | None = Field(
        default=None,
        description=(
            "License issue date (交付). "
            "Convert to YYYY-MM-DD. Do not confuse with category acquisition dates."
        )
    )

    expiration_date: str | None = Field(
        default=None,
        description=(
            "License expiration date (有効期限). "
            "Convert Japanese era dates into YYYY-MM-DD format."
        )
    )

    conditions: str | None = Field(
        default=None,
        description=(
            "Driving conditions and restrictions (条件等), "
            "such as 眼鏡等 or AT車に限る. "
            "Preserve original Japanese text."
        )
    )

class DriverLicenseBackFields(DocumentBaseModel):

    address_change_history: str | None = Field(
        default=None,
        description=(
            "Address change information (住所変更). "
            "Extract officially recorded previous or updated address information."
        )
    )

    conditions_change_history: str | None = Field(
        default=None,
        description=(
            "Changes to driving conditions or restrictions, "
            "if officially recorded on the back."
        )
    )

    remarks: str | None = Field(
        default=None,
        description=(
            "Other official remarks, annotations, or endorsements "
            "visible on the back. Preserve original Japanese text."
        )
    )

class DriverLicenseExtraction(DocumentBaseModel):

    document_type: Literal[DocumentType.DRIVER_LICENSE] = Field(
        description="Must be DRIVER_LICENSE."
    )

    front: DriverLicenseFrontFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the FRONT side "
            "of the Japanese Driver's License."
        )
    )

    back: DriverLicenseBackFields | None = Field(
        default=None,
        description=(
            "Information extracted exclusively from the BACK side "
            "of the Japanese Driver's License."
        )
    )


DocumentExtraction = Annotated[
    ResidenceCardExtraction
    | MyNumberCardExtraction
    | DriverLicenseExtraction,
    Field(discriminator="document_type"),
]

class DocumentExtractionResult(DocumentBaseModel):

    document: DocumentExtraction = Field(
        description=(
            "Structured extraction result for the identified document. "
            "Must match the appropriate document-specific schema."
        )
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description=(
            "Overall extraction confidence between 0.0 and 1.0. "
            "Reflect confidence in the accuracy and readability of extracted "
            "information, not the authenticity or validity of the document. "
            "Lower confidence when important fields are blurry, obscured, "
            "ambiguous, or unreadable."
        )
    )

    missing_fields: list[str] = Field(
        default_factory=list,
        description=(
            "List of expected field names that could not be extracted "
            "because they are missing, unreadable, obscured, or unavailable. "
            "Use the exact Pydantic field names. "
            "Do not include optional fields that are not applicable."
        )
    )

    warnings: list[str] = Field(
        default_factory=list,
        description=(
            "List of extraction-related warnings, such as blurry images, "
            "cropped document edges, inconsistent front/back information, "
            "unrecognized text, or ambiguous dates. "
            "Do not claim fraud or document forgery based solely on visual appearance."
        )
    )
