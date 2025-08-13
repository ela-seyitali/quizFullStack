#!/usr/bin/env python3
"""
Quiz Sessions Listeleme Scripti
Bu script ile mevcut quiz oturumlarını görebilirsiniz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.models.quiz_session import QuizSession
from app.models.user import User
from app.models.category import Category
from sqlalchemy.orm import Session

def list_all_quiz_sessions():
    """Tüm quiz sessions'ları listeler"""
    try:
        db = next(get_db())
        
        # Quiz sessions'ları kullanıcı ve kategori bilgileriyle birlikte al
        sessions = db.query(QuizSession, User, Category).join(
            User, QuizSession.user_id == User.id
        ).join(
            Category, QuizSession.category_id == Category.id
        ).order_by(QuizSession.started_at.desc()).all()
        
        print("📊 Quiz Sessions")
        print("=" * 80)
        
        if not sessions:
            print("❌ Henüz quiz session yok!")
            return
        
        for session, user, category in sessions:
            percentage = (session.score / session.total_questions) * 100 if session.total_questions > 0 else 0
            status = "✅ Tamamlandı" if session.completed_at else "⏳ Devam Ediyor"
            
            print(f"🆔 Session ID: {session.id}")
            print(f"👤 Kullanıcı: {user.username} ({user.email})")
            print(f"📚 Kategori: {category.name}")
            print(f"🎯 Skor: {session.score}/{session.total_questions} ({percentage:.1f}%)")
            print(f"📈 Durum: {status}")
            print(f"⏰ Başlangıç: {session.started_at}")
            if session.completed_at:
                print(f"🏁 Bitiş: {session.completed_at}")
                duration = session.completed_at - session.started_at
                print(f"⏱️ Süre: {duration}")
            print("-" * 80)
        
        print(f"\n📊 Toplam: {len(sessions)} quiz session")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def list_user_quiz_sessions(username):
    """Belirli bir kullanıcının quiz sessions'larını listeler"""
    try:
        db = next(get_db())
        
        # Kullanıcıyı bul
        user = db.query(User).filter(User.username == username).first()
        if not user:
            print(f"❌ Kullanıcı bulunamadı: {username}")
            return
        
        # Kullanıcının quiz sessions'larını al
        sessions = db.query(QuizSession, Category).join(
            Category, QuizSession.category_id == Category.id
        ).filter(QuizSession.user_id == user.id).order_by(QuizSession.started_at.desc()).all()
        
        print(f"📊 {user.username} Kullanıcısının Quiz Sessions'ları")
        print("=" * 60)
        
        if not sessions:
            print(f"❌ {user.username} kullanıcısının henüz quiz session'ı yok!")
            return
        
        total_score = 0
        total_questions = 0
        
        for session, category in sessions:
            percentage = (session.score / session.total_questions) * 100 if session.total_questions > 0 else 0
            status = "✅ Tamamlandı" if session.completed_at else "⏳ Devam Ediyor"
            
            print(f"🆔 Session ID: {session.id}")
            print(f"📚 Kategori: {category.name}")
            print(f"🎯 Skor: {session.score}/{session.total_questions} ({percentage:.1f}%)")
            print(f"📈 Durum: {status}")
            print(f"⏰ Başlangıç: {session.started_at}")
            if session.completed_at:
                print(f"🏁 Bitiş: {session.completed_at}")
            print("-" * 60)
            
            total_score += session.score
            total_questions += session.total_questions
        
        if total_questions > 0:
            overall_percentage = (total_score / total_questions) * 100
            print(f"\n📊 Genel İstatistikler:")
            print(f"🎯 Toplam Doğru: {total_score}")
            print(f"📊 Toplam Soru: {total_questions}")
            print(f"📈 Genel Başarı: {overall_percentage:.1f}%")
        
        print(f"\n📊 Toplam: {len(sessions)} quiz session")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    print("🚀 Quiz Sessions Listeleme Scripti")
    print("=" * 50)
    
    print("\nSeçenekler:")
    print("1. Tüm quiz sessions'ları listele")
    print("2. Belirli kullanıcının quiz sessions'larını listele")
    
    choice = input("\nSeçiminiz (1/2): ").strip()
    
    if choice == "1":
        list_all_quiz_sessions()
    elif choice == "2":
        username = input("👤 Kullanıcı adı: ").strip()
        list_user_quiz_sessions(username)
    else:
        print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    main()
