#!/usr/bin/env python3
"""
Quiz Sessions Oluşturma Scripti
Bu script ile quiz oturumları oluşturabilirsiniz.
"""

import sys
import os
from datetime import datetime, timedelta
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.crud.quiz_session import create_quiz_session, update_quiz_session_score
from app.crud.category import get_categories
from app.crud.user import get_users
from app.models.quiz_session import QuizSession
from sqlalchemy.orm import Session

def show_users_and_categories(db):
    """Mevcut kullanıcıları ve kategorileri gösterir"""
    users = get_users(db, skip=0, limit=100)
    categories = get_categories(db, skip=0, limit=100)
    
    print("\n👥 Mevcut Kullanıcılar:")
    print("-" * 30)
    for user in users:
        print(f"🆔 {user.id}: {user.username} ({user.email})")
    
    print("\n📚 Mevcut Kategoriler:")
    print("-" * 30)
    for cat in categories:
        print(f"🆔 {cat.id}: {cat.name} - {cat.description}")
    print()

def create_sample_quiz_sessions():
    """Örnek quiz oturumları oluşturur"""
    try:
        db = next(get_db())
        
        # Kullanıcıları ve kategorileri göster
        show_users_and_categories(db)
        
        print("🚀 Örnek Quiz Sessions Oluşturuluyor...")
        print("ℹ️ Bu fonksiyon artık örnek veri oluşturmaz.")
        print("📝 Manuel quiz session oluşturmak için seçenek 2'yi kullanın.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def create_manual_quiz_session():
    """Manuel quiz session oluşturur"""
    try:
        db = next(get_db())
        
        # Kullanıcıları ve kategorileri göster
        show_users_and_categories(db)
        
        # Kullanıcı bilgilerini al
        user_id = int(input("👤 User ID: ").strip())
        category_id = int(input("📚 Category ID: ").strip())
        score = int(input("🎯 Score (doğru cevap sayısı): ").strip())
        total_questions = int(input("📊 Total Questions: ").strip())
        
        # Quiz session oluştur
        quiz_session = QuizSession(
            user_id=user_id,
            category_id=category_id,
            score=score,
            total_questions=total_questions,
            started_at=datetime.now() - timedelta(minutes=30),
            completed_at=datetime.now()
        )
        
        db.add(quiz_session)
        db.commit()
        db.refresh(quiz_session)
        
        print(f"✅ Quiz Session oluşturuldu!")
        print(f"🆔 ID: {quiz_session.id}")
        print(f"👤 User ID: {quiz_session.user_id}")
        print(f"📚 Category ID: {quiz_session.category_id}")
        print(f"🎯 Score: {quiz_session.score}/{quiz_session.total_questions}")
        print(f"📊 Percentage: {(quiz_session.score/quiz_session.total_questions)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    print("🚀 Quiz Sessions Oluşturma Scripti")
    print("=" * 50)
    
    print("\nSeçenekler:")
    print("1. Bilgi göster (kullanıcılar ve kategoriler)")
    print("2. Manuel quiz session oluştur")
    
    choice = input("\nSeçiminiz (1/2): ").strip()
    
    if choice == "1":
        try:
            db = next(get_db())
            show_users_and_categories(db)
        except Exception as e:
            print(f"❌ Hata: {e}")
    elif choice == "2":
        create_manual_quiz_session()
    else:
        print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main()
