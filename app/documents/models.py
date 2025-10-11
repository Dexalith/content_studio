from sqlalchemy import ForeignKey, DateTime, Text, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from uuid import UUID, uuid4

# from app.projects.models import Project
from app.users.models import Base
from .enum import DocumentStatus, DocumentType


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    document_type: Mapped[DocumentType] = mapped_column(SQLEnum(DocumentType), nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(SQLEnum(DocumentStatus), default=DocumentStatus.DRAFT)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    ai_model_used: Mapped[str] = mapped_column(String(50), nullable=True)

    # Foreign keys
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE",), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="documents")
    project: Mapped["Project"] = relationship("Project", back_populates="documents")