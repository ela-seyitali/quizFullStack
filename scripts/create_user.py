#!/usr/bin/env python3
"""
Kullanıcı Oluşturma Scripti
Bu script ile yeni kullanıcılar ekleyebilirsiniz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.crud.user import create_user
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

def create_new_user(username: str, email: str, password: str, is_admin: bool = False):
    """Yeni kullanıcı oluşturur"""
    try:
        db = next(get_db())
        
        # Kullanıcı oluştur
        user_data = UserCreate(
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )
        
        user = create_user(db=db, user=user_data)
        
        print(f"✅ Kullanıcı başarıyla oluşturuldu!")
        print(f"👤 Username: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"👑 Admin: {'Evet' if user.is_admin else 'Hayır'}")
        print(f"🆔 ID: {user.id}")
        
        return user
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def main():
    print("🚀 Kullanıcı Oluşturma Scripti")
    print("=" * 40)
    
    # Kullanıcı bilgilerini al
    username = input("👤 Username: ").strip()
    email = input("📧 Email: ").strip()
    password = input("🔒 Şifre: ").strip()
    
    # Admin yetkisi
    admin_choice = input("👑 Admin yetkisi verilsin mi? (y/n): ").strip().lower()
    is_admin = admin_choice in ['y', 'yes', 'evet', 'e']
    
    if not username or not email or not password:
        print("❌ Tüm alanları doldurun!")
        return
    
    # Kullanıcı oluştur
    user = create_new_user(username, email, password, is_admin)
    
    if user:
        print("\n🎉 Kullanıcı oluşturuldu!")
        print(f"🔗 Swagger UI: http://127.0.0.1:8000/docs")
        print(f"📝 Login endpoint: POST /token")
    else:
        print("\n❌ Kullanıcı oluşturulamadı!")

if __name__ == "__main__":
    main()
