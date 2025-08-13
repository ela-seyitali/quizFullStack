"""
QuizSession CRUD operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.models.quiz_session import QuizSession
from app.schemas.quiz_session import QuizSessionCreate

def create_quiz_session(db: Session, quiz_session: QuizSessionCreate, user_id: int):
    """Create a new quiz session"""
    db_quiz_session = QuizSession(**quiz_session.model_dump(), user_id=user_id)
    db.add(db_quiz_session)
    db.commit()
    db.refresh(db_quiz_session)
    return db_quiz_session

def update_quiz_session_score(db: Session, session_id: int, score: int, total_questions: int):
    """Update quiz session score"""
    db_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if db_session:
        db_session.score = score
        db_session.total_questions = total_questions
        db.commit()
        db.refresh(db_session)
    return db_session

def get_user_quiz_sessions(db: Session, user_id: int):
    """Get all quiz sessions for a user"""
    return db.query(QuizSession).filter(QuizSession.user_id == user_id).all()

def get_quiz_statistics(db: Session, user_id: int):
    """Get quiz statistics for a user"""
    return db.query(
        QuizSession.category_id,
        func.avg(QuizSession.score).label('avg_score'),
        func.count(QuizSession.id).label('total_attempts'),
        func.max(QuizSession.score).label('best_score')
    ).filter(QuizSession.user_id == user_id).group_by(QuizSession.category_id).all()
