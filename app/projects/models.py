from sqlalchemy import ForeignKey, DateTime, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from uuid import UUID, uuid4

# from app.documents.models import Document
from app.users.models import Base


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE",), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner: Mapped["User"] = relationship("User", back_populates="projects")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="project")