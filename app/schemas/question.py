"""
Question schemas for API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

from .category import Category

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
