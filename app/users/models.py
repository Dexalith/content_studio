from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from datetime import datetime
from uuid import UUID, uuid4

# from app.projects.models import Project

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(55), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    daily_limit_gen: Mapped[int] = mapped_column(Integer, default=5)
    monthly_limit_gen: Mapped[int] = mapped_column(Integer, default=150)

    # relations
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner")
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="owner")