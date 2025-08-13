#!/usr/bin/env python3
"""
Kullanıcı Listeleme Scripti
Bu script ile mevcut kullanıcıları görebilirsiniz.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.crud.user import get_users

def list_all_users():
    """Tüm kullanıcıları listeler"""
    try:
        db = next(get_db())
        
        users = get_users(db, skip=0, limit=100)
        
        print("👥 Mevcut Kullanıcılar")
        print("=" * 50)
        
        if not users:
            print("❌ Henüz kullanıcı yok!")
            return
        
        for user in users:
            admin_status = "👑 ADMIN" if user.is_admin else "👤 USER"
            print(f"{admin_status} | ID: {user.id} | Username: {user.username} | Email: {user.email}")
        
        print(f"\n📊 Toplam: {len(users)} kullanıcı")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def main():
    print("🚀 Kullanıcı Listeleme Scripti")
    print("=" * 40)
    
    list_all_users()

if __name__ == "__main__":
    main()
