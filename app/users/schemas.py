from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

# Для регистрации
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

# Для входа
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Для ответа (без пароля)
class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    daily_generation_limit: int
    monthly_generation_limit: int
    created_at: datetime

    class Config:
        from_attributes = True

# Токен
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"