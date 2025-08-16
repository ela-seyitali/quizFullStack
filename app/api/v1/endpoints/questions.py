"""
Question endpoints.
"""

from typing import List
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.question import (
    create_question, get_questions, get_questions_by_category,
    get_question, update_question, delete_question
)
from app.crud.category import get_category
from app.schemas.question import Question, QuestionCreate, QuestionUpdate
from app.core.security import get_current_admin_user
from app.models.user import User

router = APIRouter()

@router.post("/admin/questions/", response_model=Question, tags=["admin"])
async def create_new_question(
    question: QuestionCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new question (admin only)"""
    return create_question(db=db, question=question)

@router.get("/admin/questions/", response_model=List[Question], tags=["admin"])
async def read_questions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all questions (admin only)"""
    questions = get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/admin/questions/{question_id}", response_model=Question, tags=["admin"])
async def read_question(
    question_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get a specific question by ID (admin only)"""
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.put("/admin/questions/{question_id}", response_model=Question, tags=["admin"])
async def update_existing_question(
    question_id: int,
    question_update: QuestionUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a question (admin only)"""
    db_question = update_question(db, question_id=question_id, question_update=question_update)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.delete("/admin/questions/{question_id}", tags=["admin"])
async def delete_existing_question(
    question_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a question (admin only)"""
    db_question = delete_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}

@router.get("/quiz/questions/{category_id}", tags=["quiz"])
async def get_quiz_questions(
    category_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get questions for quiz (without correct answers)"""
    # Check if category exists
    category = get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    questions = get_questions_by_category(db, category_id=category_id, limit=limit)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this category")
    
    # Randomize questions
    random.shuffle(questions)
    
    # Return questions without correct answers
    quiz_questions = []
    for question in questions:
        quiz_questions.append({
            "id": question.id,
            "question_text": question.question_text,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "category_id": question.category_id
        })
    
    return quiz_questions
