from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Category, Question, User, QuizSession
from schemas import CategoryCreate, QuestionCreate, UserCreate, QuizSessionCreate
from auth import get_password_hash
from typing import List, Optional

# Category CRUD operations
def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

# Question CRUD operations
def create_question(db: Session, question: QuestionCreate):
    db_question = Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Question).filter(Question.is_active == True).offset(skip).limit(limit).all()

def get_questions_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(Question).filter(
        Question.category_id == category_id,
        Question.is_active == True
    ).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()

def update_question(db: Session, question_id: int, question_update):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        for field, value in question_update.model_dump(exclude_unset=True).items():
            setattr(db_question, field, value)
        db.commit()
        db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
    return db_question

# User CRUD operations
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Quiz Session CRUD operations
def create_quiz_session(db: Session, quiz_session: QuizSessionCreate, user_id: int):
    db_quiz_session = QuizSession(**quiz_session.model_dump(), user_id=user_id)
    db.add(db_quiz_session)
    db.commit()
    db.refresh(db_quiz_session)
    return db_quiz_session

def update_quiz_session_score(db: Session, session_id: int, score: int, total_questions: int):
    db_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if db_session:
        db_session.score = score
        db_session.total_questions = total_questions
        db.commit()
        db.refresh(db_session)
    return db_session

def get_user_quiz_sessions(db: Session, user_id: int):
    return db.query(QuizSession).filter(QuizSession.user_id == user_id).all()

def get_quiz_statistics(db: Session, user_id: int):
    return db.query(
        QuizSession.category_id,
        func.avg(QuizSession.score).label('avg_score'),
        func.count(QuizSession.id).label('total_attempts'),
        func.max(QuizSession.score).label('best_score')
    ).filter(QuizSession.user_id == user_id).group_by(QuizSession.category_id).all() 