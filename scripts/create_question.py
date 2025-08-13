#!/usr/bin/env python3
"""
Soru Oluşturma Scripti
Bu script ile yeni sorular ekleyebilirsiniz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.crud.question import create_question
from app.crud.category import get_categories
from app.schemas.question import QuestionCreate

def show_categories(db):
    """Mevcut kategorileri gösterir"""
    categories = get_categories(db, skip=0, limit=100)
    print("\n📚 Mevcut Kategoriler:")
    print("-" * 30)
    for cat in categories:
        print(f"🆔 {cat.id}: {cat.name} - {cat.description}")
    print()

def create_new_question(question_text: str, option_a: str, option_b: str, 
                       option_c: str, option_d: str, correct_answer: str, 
                       category_id: int, explanation: str = "", is_active: bool = True):
    """Yeni soru oluşturur"""
    try:
        db = next(get_db())
        
        # Kategorileri göster
        show_categories(db)
        
        # Soru oluştur
        question_data = QuestionCreate(
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            category_id=category_id,
            explanation=explanation,
            is_active=is_active
        )
        
        question = create_question(db=db, question=question_data)
        
        print(f"✅ Soru başarıyla oluşturuldu!")
        print(f"❓ Question: {question.question_text}")
        print(f"🆔 ID: {question.id}")
        print(f"📚 Category ID: {question.category_id}")
        
        return question
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def main():
    print("🚀 Soru Oluşturma Scripti")
    print("=" * 40)
    
    # Soru bilgilerini al
    question_text = input("❓ Soru Metni: ").strip()
    option_a = input("🅰️  A Seçeneği: ").strip()
    option_b = input("🅱️  B Seçeneği: ").strip()
    option_c = input("©️  C Seçeneği: ").strip()
    option_d = input("🆔 D Seçeneği: ").strip()
    
    while True:
        correct_answer = input("✅ Doğru Cevap (A/B/C/D): ").strip().upper()
        if correct_answer in ['A', 'B', 'C', 'D']:
            break
        print("❌ Lütfen A, B, C veya D girin!")
    
    category_id = input("📚 Kategori ID: ").strip()
    explanation = input("📝 Açıklama (opsiyonel): ").strip()
    
    if not question_text or not option_a or not option_b or not option_c or not option_d or not category_id:
        print("❌ Gerekli alanları doldurun!")
        return
    
    try:
        category_id = int(category_id)
    except ValueError:
        print("❌ Kategori ID sayı olmalı!")
        return
    
    # Soru oluştur
    question = create_new_question(
        question_text, option_a, option_b, option_c, option_d,
        correct_answer, category_id, explanation
    )
    
    if question:
        print("\n🎉 Soru oluşturuldu!")
        print(f"🔗 Swagger UI: http://127.0.0.1:8000/docs")
        print(f"📝 Sorular: GET /admin/questions/")
    else:
        print("\n❌ Soru oluşturulamadı!")

if __name__ == "__main__":
    main()
