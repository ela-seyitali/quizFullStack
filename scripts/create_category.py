#!/usr/bin/env python3
"""
Kategori Oluşturma Scripti
Bu script ile yeni kategoriler ekleyebilirsiniz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.crud.category import create_category
from app.schemas.category import CategoryCreate

def create_new_category(name: str, description: str = ""):
    """Yeni kategori oluşturur"""
    try:
        db = next(get_db())
        
        # Kategori oluştur
        category_data = CategoryCreate(
            name=name,
            description=description
        )
        
        category = create_category(db=db, category=category_data)
        
        print(f"✅ Kategori başarıyla oluşturuldu!")
        print(f"📚 Name: {category.name}")
        print(f"📝 Description: {category.description}")
        print(f"🆔 ID: {category.id}")
        
        return category
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def main():
    print("🚀 Kategori Oluşturma Scripti")
    print("=" * 40)
    
    # Kategori bilgilerini al
    name = input("📚 Kategori Adı: ").strip()
    description = input("📝 Açıklama (opsiyonel): ").strip()
    
    if not name:
        print("❌ Kategori adı gerekli!")
        return
    
    # Kategori oluştur
    category = create_new_category(name, description)
    
    if category:
        print("\n🎉 Kategori oluşturuldu!")
        print(f"🔗 Swagger UI: http://127.0.0.1:8000/docs")
        print(f"📝 Kategoriler: GET /admin/categories/")
    else:
        print("\n❌ Kategori oluşturulamadı!")

if __name__ == "__main__":
    main()
