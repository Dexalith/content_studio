from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.schemas import AIGenerationResponse, AIGenerationRequest
from app.ai.services import ai_service
from app.db.db_client import async_db
from app.core.depencies import get_current_user
from app.users.models import User
from app.doc_proj.models import Project, Document
from app.doc_proj.enum import DocumentStatus


router = APIRouter(prefix="/ai", tags=["AI Generation"])


@router.post("/generate", response_model=AIGenerationResponse)
async def generate_content(
        generation_request: AIGenerationRequest,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(async_db.get_session)
):
    """
        Генерация контента через AI
    """
    document_title = f"AI Generated: {generation_request.prompt[:50]}..."

    db_document = Document(
        title=document_title,
        document_type=generation_request.document_type,
        owner_id=current_user.id,
        project_id=generation_request.project_id,
        status=DocumentStatus.GENERATING,
        prompt=generation_request.prompt
    )

    session.add(db_document)
    await session.commit()
    await session.refresh(db_document)

    try:
        # Генерируем контент через AI
        generated_content = await ai_service.generate_content(
            prompt=generation_request.prompt,
            document_type=generation_request.document_type.value,
            max_tokens=generation_request.max_tokens,
            temperature=generation_request.temperature
        )

        # Обновляем документ с сгенерированным контентом
        db_document.content = generated_content
        db_document.status = DocumentStatus.COMPLETED
        db_document.ai_model_used = "gpt-3.5-turbo"

        await session.commit()

        return AIGenerationResponse(
            content=generated_content,
            document_id=str(db_document.id)
        )

    except Exception as e:
        # Если ошибка - обновляем статус документа
        db_document.status = DocumentStatus.FAILED
        await session.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content generation failed: {str(e)}"
        )