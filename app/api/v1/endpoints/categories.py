"""
Category endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.crud.category import create_category, get_categories, get_category
from app.schemas.category import Category, CategoryCreate
from app.schemas.user import User

router = APIRouter()

@router.post("/admin/categories/", response_model=Category, tags=["admin"])
async def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new category (admin only)"""
    return create_category(db=db, category=category)

@router.get("/admin/categories/", response_model=List[Category], tags=["admin"])
async def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all categories (admin only)"""
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=Category, tags=["default"])
async def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.get("/quiz/categories/", response_model=List[Category], tags=["quiz"])
async def get_quiz_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories for quiz selection"""
    categories = get_categories(db, skip=skip, limit=limit)
    return categories
