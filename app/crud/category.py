"""
Category CRUD operations.
"""

from sqlalchemy.orm import Session
from typing import List

from app.models.category import Category
from app.schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate):
    """Create a new category"""
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Get all categories with pagination"""
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    """Get category by ID"""
    return db.query(Category).filter(Category.id == category_id).first()
