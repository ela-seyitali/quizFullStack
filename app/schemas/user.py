"""
User schemas for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Şifre en az 6 karakter olmalı")
    is_admin: bool = Field(False, description="Admin yetkisi (true/false)")

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
