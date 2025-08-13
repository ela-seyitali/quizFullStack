"""
QuizSession schemas for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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
