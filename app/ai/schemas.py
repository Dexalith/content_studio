from pydantic import BaseModel, Field
from typing import Optional

from app.doc_proj.enum import DocumentType


class AIGenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=10, max_length=2000, description="Описание того, что нужно сгенерировать")
    document_type: DocumentType
    max_tokens: int = Field(1000, ge=100, le=4000)
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    project_id: Optional[str] = None

class AIGenerationResponse(BaseModel):
    content: str
    document_id: str
    tokens_used: int = 0