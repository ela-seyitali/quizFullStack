from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# Question schemas
class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=1, description="Soru metni")
    option_a: str = Field(..., min_length=1, max_length=200, description="A seçeneği")
    option_b: str = Field(..., min_length=1, max_length=200, description="B seçeneği")
    option_c: str = Field(..., min_length=1, max_length=200, description="C seçeneği")
    option_d: str = Field(..., min_length=1, max_length=200, description="D seçeneği")
    correct_answer: str = Field(..., pattern="^[ABCD]$", description="Doğru cevap (A, B, C veya D)")
    explanation: Optional[str] = Field(None, description="Açıklama (opsiyonel)")
    category_id: int = Field(..., gt=0, description="Kategori ID (1'den büyük olmalı)")
    is_active: bool = Field(True, description="Soru aktif mi?")

    @validator('category_id')
    def validate_category_id(cls, v):
        if v <= 0:
            raise ValueError('category_id 0\'dan büyük olmalıdır')
        return v

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=1, description="Soru metni")
    option_a: Optional[str] = Field(None, min_length=1, max_length=200, description="A seçeneği")
    option_b: Optional[str] = Field(None, min_length=1, max_length=200, description="B seçeneği")
    option_c: Optional[str] = Field(None, min_length=1, max_length=200, description="C seçeneği")
    option_d: Optional[str] = Field(None, min_length=1, max_length=200, description="D seçeneği")
    correct_answer: Optional[str] = Field(None, pattern="^[ABCD]$", description="Doğru cevap (A, B, C veya D)")
    explanation: Optional[str] = Field(None, description="Açıklama (opsiyonel)")
    category_id: Optional[int] = Field(None, gt=0, description="Kategori ID (1'den büyük olmalı)")
    is_active: Optional[bool] = Field(None, description="Soru aktif mi?")

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Şifre en az 6 karakter olmalı")

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Quiz session schemas
class QuizSessionBase(BaseModel):
    category_id: int = Field(..., gt=0, description="Kategori ID")

class QuizSessionCreate(QuizSessionBase):
    pass

class QuizSession(QuizSessionBase):
    id: int
    user_id: int
    score: int
    total_questions: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 