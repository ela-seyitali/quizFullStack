"""
Question CRUD operations.
"""

from sqlalchemy.orm import Session
from typing import List

from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate

def create_question(db: Session, question: QuestionCreate):
    """Create a new question"""
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    """Get all active questions with pagination"""
    return db.query(Question).filter(Question.is_active == True).offset(skip).limit(limit).all()

def get_questions_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    """Get questions by category with pagination"""
    return db.query(Question).filter(
        Question.category_id == category_id,
        Question.is_active == True
    ).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int):
    """Get question by ID"""
    return db.query(Question).filter(Question.id == question_id).first()

def update_question(db: Session, question_id: int, question_update: QuestionUpdate):
    """Update a question"""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        for field, value in question_update.model_dump(exclude_unset=True).items():
            setattr(db_question, field, value)
        db.commit()
        db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    """Delete a question"""
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question
