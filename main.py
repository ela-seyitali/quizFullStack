from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from typing import List
import random
import logging

from database import get_db, engine
from models import Base, Category, QuizSession
from schemas import (
    Category as CategorySchema, CategoryCreate, Question, QuestionCreate, QuestionUpdate,
    User, UserCreate, QuizSession as QuizSessionSchema, QuizSessionCreate, Token
)
from crud import (
    create_category, get_categories, get_category,
    create_question, get_questions, get_questions_by_category,
    get_question, update_question, delete_question,
    create_user, get_user_by_username, get_user_by_email,
    create_quiz_session, update_quiz_session_score,
    get_user_quiz_sessions, get_quiz_statistics
)
from auth import (
    authenticate_user, create_access_token, get_current_user,
    get_current_admin_user, ACCESS_TOKEN_EXPIRE_MINUTES
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title="Quiz API", 
    description="A comprehensive quiz application API",
    version="1.0.0",
    tags_metadata=[
        {
            "name": "default",
            "description": "Default endpoints for general access"
        },
        {
            "name": "admin",
            "description": "Admin-only endpoints for managing categories and questions"
        },
        {
            "name": "quiz",
            "description": "Quiz-related endpoints for users to take quizzes"
        },
        {
            "name": "auth",
            "description": "Authentication endpoints for user registration and login"
        }
    ]
)

# Root endpoint - Ana sayfa
@app.get("/", tags=["default"])
async def root():
    return {
        "message": "🎉 Quiz API başarıyla çalışıyor! 🎉",
        "status": "success",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "default": {
                "root": "/",
                "health": "/health",
                "category": "/categories/{category_id}"
            },
            "admin": {
                "categories": "/admin/categories/",
                "questions": "/admin/questions/"
            },
            "quiz": {
                "categories": "/quiz/categories/",
                "start": "/quiz/start/{category_id}",
                "questions": "/quiz/questions/{category_id}",
                "submit": "/quiz/submit/{session_id}",
                "history": "/quiz/history/",
                "statistics": "/quiz/statistics/"
            },
            "auth": {
                "register": "/register",
                "login": "/token"
            }
        },
        "description": "Bu API, quiz uygulaması için geliştirilmiştir. Kullanım için /docs endpoint'ini ziyaret edin."
    }

# Health check endpoint
@app.get("/health", tags=["default"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Quiz API çalışıyor ve sağlıklı!",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Authentication endpoints
@app.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=User, tags=["auth"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db=db, user=user)

# Category endpoints
@app.post("/admin/categories/", response_model=CategorySchema, tags=["admin"])
async def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return create_category(db=db, category=category)

@app.get("/admin/categories/", response_model=List[CategorySchema], tags=["admin"])
async def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=CategorySchema, tags=["default"])
async def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Question endpoints (Admin only)
@app.post("/admin/questions/", response_model=Question, tags=["admin"])
async def create_new_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return create_question(db=db, question=question)

@app.get("/admin/questions/", response_model=List[Question], tags=["admin"])
async def read_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    questions = get_questions(db, skip=skip, limit=limit)
    return questions

@app.get("/admin/questions/{question_id}", response_model=Question, tags=["admin"])
async def read_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_question = get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.put("/admin/questions/{question_id}", response_model=Question, tags=["admin"])
async def update_existing_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_question = update_question(db, question_id=question_id, question_update=question_update)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.delete("/admin/questions/{question_id}", tags=["admin"])
async def delete_existing_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    db_question = delete_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}

# Quiz endpoints
@app.get("/quiz/categories/", response_model=List[CategorySchema], tags=["quiz"])
async def get_quiz_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@app.post("/quiz/start/{category_id}", response_model=QuizSessionSchema, tags=["quiz"])
async def start_quiz(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if category exists
    category = get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Create quiz session
    quiz_session = QuizSessionCreate(category_id=category_id)
    return create_quiz_session(db=db, quiz_session=quiz_session, user_id=current_user.id)

@app.get("/quiz/questions/{category_id}", tags=["quiz"])
async def get_quiz_questions(
    category_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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

@app.post("/quiz/submit/{session_id}", tags=["quiz"])
async def submit_quiz(
    session_id: int,
    answers: dict,  # {"question_id": "A", "question_id": "B", ...}
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get quiz session
    quiz_session = db.query(QuizSession).filter(QuizSession.id == session_id).first()
    if not quiz_session:
        raise HTTPException(status_code=404, detail="Quiz session not found")
    
    if quiz_session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this quiz session")
    
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

@app.get("/quiz/history/", response_model=List[QuizSessionSchema], tags=["quiz"])
async def get_quiz_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_quiz_sessions(db, current_user.id)

@app.get("/quiz/statistics/", tags=["quiz"])
async def get_quiz_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    stats = get_quiz_statistics(db, current_user.id)
    return stats

# Initialize default categories
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🚀 Quiz API başlatılıyor...")
        logger.info("✅ Uygulama başarıyla başlatıldı!")
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        logger.error("Please check your database connection and credentials")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Quiz API...")
    print("📊 Database: PostgreSQL (quiz_db)")
    print("🌐 Server: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
