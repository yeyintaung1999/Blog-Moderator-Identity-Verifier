from enum import Enum

from pydantic import BaseModel, Field


class ModerationCategory(str, Enum):
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    ADULT_CONTENT = "adult_content"
    PORNOGRAPHY = "pornography"
    DRUGS = "drugs"
    ILLEGAL_CONTENT = "illegal_content"

class EvidenceSource(str, Enum):
    TEXT = "text"
    IMAGE = "image"

class CategoryAssessment(BaseModel):
    present: bool
    policy_violation: bool

    confidence: float = Field(ge=0, le=1)
    severity: float = Field(ge=0, le=1)

    reason: str
    evidence: list[str] = Field(default_factory=list)

class EvidenceAssessment(BaseModel):
    source: EvidenceSource
    image_index: int | None = None
    description: str

class BlogModerationAssessment(BaseModel):
    categories: dict[ModerationCategory, CategoryAssessment]
    evidence: list[str] = Field(default_factory=list)


class ModerationDecision(str, Enum):
    APPROVE = "APPROVE"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    REJECT = "REJECT"


class BlogModerationResponse(BaseModel):
    blog_id: str
    score: float = Field(ge=0, le=1)
    decision: ModerationDecision
    assessment: BlogModerationAssessment
