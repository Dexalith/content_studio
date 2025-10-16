from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List

from app.db.db_client import async_db
from app.doc_proj.schemas import ProjectOut, ProjectCreate, ProjectUpdate
from app.core.depencies import get_current_user
from app.users.models import User
from app.doc_proj.models import Project, Document


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project(
        project_data: ProjectCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """"Создать новый проект"""
    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)

    return project


@router.get("", response_model=List[ProjectOut])
async def get_projects(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(async_db.get_session)
):
    """Получить все проекты пользователя"""
    projects = await session.execute(
        select(Project).where(Project.owner_id == current_user.id)
    )

    return projects.scalars().all()


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project_by_id(
        project_id: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Получить проект по ID"""
    result = await session.execute(
        select(Project).where(
            (Project.id == project_id) & (Project.owner_id == current_user.id)
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    return project


@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(
        project_id: str,
        project_data: ProjectUpdate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """"Обновить проект"""
    result = await session.execute(
        select(Project).where(
            (Project.id == project_id) & (Project.owner_id == current_user.id)
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    await session.commit()
    await session.refresh(project)

    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
        project_id: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """Удалить проект"""
    result = await session.execute(
        select(Project).where(
            (Project.id == project_id) & (Project.owner_id == current_user.id)
        )
    )
    project = result.scalar_one_or_none()

    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")

    await session.delete(project)
    await session.commit()