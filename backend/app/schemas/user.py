from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, Dict

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    preferences: Optional[Dict[str, Any]] = None
    is_active: bool

    class Config:
        from_attributes = True
