"""
Quiz endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.quiz_session import (
    create_quiz_session, update_quiz_session_score,
    get_user_quiz_sessions, get_quiz_statistics
)
from app.crud.category import get_category
from app.crud.question import get_question
from app.models.quiz_session import QuizSession
from app.schemas.quiz_session import QuizSession as QuizSessionSchema, QuizSessionCreate
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/quiz/start/{category_id}", response_model=QuizSessionSchema, tags=["quiz"])
async def start_quiz(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new quiz session (user authentication required)"""
    # Check if category exists
    category = get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create quiz session with user_id
    quiz_session = QuizSessionCreate(category_id=category_id)
    return create_quiz_session(db=db, quiz_session=quiz_session, user_id=current_user.id)

@router.post("/quiz/submit/{session_id}", tags=["quiz"])
async def submit_quiz(
    session_id: int,
    answers: dict,  # {"question_id": "A", "question_id": "B", ...}
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit quiz answers and get score (user authentication required)"""
    # Get quiz session
    quiz_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not quiz_session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    
    # Verify quiz session belongs to current user
    if quiz_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this quiz session")
    
    # Calculate score
    score = 0
    total_questions = len(answers)
    
    for question_id, answer in answers.items():
        question = get_question(db, int(question_id))
        if question and question.correct_answer == answer:
            score += 1
    
    # Update quiz session
    update_quiz_session_score(db, session_id, score, total_questions)
    
    return {
        "session_id": session_id,
        "score": score,
        "total_questions": total_questions,
        "percentage": (score / total_questions) * 100 if total_questions > 0 else 0
    }

@router.get("/quiz/history/", response_model=List[QuizSessionSchema], tags=["quiz"])
async def get_quiz_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get quiz history (user's own sessions)"""
    return get_user_quiz_sessions(db, current_user.id)

@router.get("/quiz/statistics/", tags=["quiz"])
async def get_quiz_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get quiz statistics (user's own sessions)"""
    stats = get_quiz_statistics(db, current_user.id)
    return stats
