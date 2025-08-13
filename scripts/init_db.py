#!/usr/bin/env python3
"""
Veritabanı başlatma ve admin kullanıcı oluşturma scripti
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine, SessionLocal, Base
from app.models import User, Category
from app.core.security import get_password_hash
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Veritabanı tablolarını oluştur ve başlangıç verilerini ekle"""
    try:
        logger.info("🗄️ Veritabanı tabloları oluşturuluyor...")
        
        # Tabloları oluştur
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Veritabanı tabloları başarıyla oluşturuldu!")
        
        # Veritabanı bağlantısını test et
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("✅ Veritabanı bağlantısı başarılı!")
        
        # Admin kullanıcı oluştur
        create_admin_user(db)
        
        # Varsayılan kategoriler oluştur
        create_default_categories(db)
        
        db.close()
        logger.info("🎉 Veritabanı başlatma tamamlandı!")
        
    except Exception as e:
        logger.error(f"❌ Veritabanı başlatma hatası: {e}")
        raise

def create_admin_user(db):
    """Admin kullanıcı oluştur"""
    try:
        # Admin kullanıcı var mı kontrol et
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            # Admin kullanıcı oluştur
            admin_user = User(
                username="admin",
                email="admin@quiz.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("✅ Admin kullanıcı oluşturuldu: admin/admin123")
        else:
            logger.info("ℹ️ Admin kullanıcı zaten mevcut")
            
    except Exception as e:
        logger.error(f"❌ Admin kullanıcı oluşturma hatası: {e}")
        db.rollback()
        raise

def create_default_categories(db):
    """Varsayılan kategoriler oluştur"""
    try:
        # Temel kategoriler (sadece gerekli olanlar)
        default_categories = [
            {"name": "General Knowledge", "description": "Genel bilgi soruları"},
            {"name": "Technology", "description": "Teknoloji ile ilgili sorular"}
        ]
        
        for cat_data in default_categories:
            existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                logger.info(f"✅ Kategori oluşturuldu: {cat_data['name']}")
        
        db.commit()
        logger.info("✅ Temel kategoriler oluşturuldu!")
        
    except Exception as e:
        logger.error(f"❌ Kategori oluşturma hatası: {e}")
        db.rollback()
        raise

def show_database_info():
    """Veritabanı bilgilerini göster"""
    try:
        db = SessionLocal()
        
        # Kullanıcı sayısı
        user_count = db.query(User).count()
        logger.info(f"👥 Toplam kullanıcı sayısı: {user_count}")
        
        # Admin kullanıcılar
        admin_users = db.query(User).filter(User.is_admin == True).all()
        logger.info(f"👑 Admin kullanıcılar: {[u.username for u in admin_users]}")
        
        # Kategori sayısı
        category_count = db.query(Category).count()
        logger.info(f"📚 Toplam kategori sayısı: {category_count}")
        
        # Kategoriler
        categories = db.query(Category).all()
        for cat in categories:
            logger.info(f"  - {cat.name}: {cat.description}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Veritabanı bilgileri alınamadı: {e}")

if __name__ == "__main__":
    print("🚀 Quiz API Veritabanı Başlatılıyor...")
    print("=" * 50)
    
    try:
        init_database()
        print("\n" + "=" * 50)
        show_database_info()
        print("\n🎉 Veritabanı başarıyla hazırlandı!")
        print("\n📋 Kullanım Bilgileri:")
        print("  • Admin Kullanıcı: admin")
        print("  • Şifre: admin123")
        print("  • API URL: http://127.0.0.1:8000")
        print("  • Docs: http://127.0.0.1:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        print("🔧 Lütfen .env dosyasını ve PostgreSQL bağlantısını kontrol edin.")
