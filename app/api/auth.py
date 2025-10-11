from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.db_client import async_db
from app.core.auth_conf import hash_password, verify_password, create_token
from app.users.schemas import UserOut, UserCreate, Token, UserLogin
from app.users.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(async_db.get_session)
):
    user = await session.execute(
        select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
    )
    if user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем или почтой существует"
        )

    hashed_password = hash_password(user_data.password)
    create_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=True

    )

    session.add(create_user)
    await session.commit()
    await session.refresh(create_user)

    return create_user


@router.post("/login", response_model=Token)
async def login_user(
        user_data: UserLogin,
        session: AsyncSession = Depends(async_db.get_session)
):
    select_user = await session.execute(select(User).where(User.email == user_data.email))
    user = select_user.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль или почта"
        )

    access_token = create_token(
        data={"sub": str(user.id)}
    )

    return Token(access_token=access_token)