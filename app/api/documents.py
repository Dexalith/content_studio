from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.db_client import async_db
from app.core.depencies import get_current_user
from app.users.models import User
from app.doc_proj.models import Document, DocumentStatus
from app.doc_proj.schemas import DocumentCreate, DocumentUpdate, DocumentOut


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=List[DocumentOut])
async def get_documents(
    project_id: str = None,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(async_db.get_session)
):
    """Получить документы пользователя (с фильтром по проекту)"""
    query = select(Document).where(Document.owner_id == current_user.id)

    if project_id:
        query = query.where(Document.project_id == project_id)

    result = await session.execute(query)
    documents = result.scalars().all()
    return documents


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(
        document_data: DocumentCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Создать новый документ (пока без AI генерации)"""
    # Если указан project_id, проверяем что проект принадлежит пользователю
    if document_data.project_id:
        result = await session.execute(
            select(Document).where(Document.id == document_data.project_id)
        )
        project = result.scalar_one_or_none()
        if not project or project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Проект не найден"
            )

    db_document = Document(
        title=document_data.title,
        document_type=document_data.document_type,
        owner_id=current_user.id,
        project_id=document_data.project_id,
        status=DocumentStatus.DRAFT
    )

    session.add(db_document)
    await session.commit()
    await session.refresh(db_document)

    return db_document


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(
        document_id: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Получить документ по ID"""
    result = await session.execute(
        select(Document).where(
            (Document.id == document_id) & (Document.owner_id == current_user.id)
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    return document


@router.patch("/{document_id}", response_model=DocumentOut)
async def update_document(
        document_id: str,
        document_data: DocumentUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Обновить документ (ручное редактирование)"""
    result = await session.execute(
        select(Document).where(
            (Document.id == document_id) & (Document.owner_id == current_user.id)
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    update_data = document_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)

    await session.commit()
    await session.refresh(document)

    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
        document_id: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Удалить документ"""
    result = await session.execute(
        select(Document).where(
            (Document.id == document_id) & (Document.owner_id == current_user.id)
        )
    )
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Документ не найден")

    await session.delete(document)
    await session.commit()