import enum


class DocumentType(str, enum.Enum):
    ARTICLE = "article"
    SOCIAL_MEDIA = "social_media"
    EMAIL = "email"
    AD_COPY = "ad_copy"
    PRODUCT_DESCRIPTION = "product_description"

class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"