from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from app.doc_proj.enum import DocumentType, DocumentStatus


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=5, max_length=100, description="Название проекта")
    description: Optional[str] = Field(None, max_length=500, description="Описание проекта")


class ProjectOut(BaseModel):
    id: UUID
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectUpdate(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    documents_count: int = 0

    class Config:
        from_attributes = True


class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    document_type: DocumentType
    project_id: Optional[UUID] = None


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None

class DocumentOut(BaseModel):
    id: UUID
    title: str
    content: Optional[str]
    document_type: DocumentType
    status: DocumentStatus
    prompt: Optional[str]
    ai_model_used: Optional[str]
    owner_id: UUID
    project_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True