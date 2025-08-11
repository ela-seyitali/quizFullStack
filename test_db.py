from database import engine
from models import Base

def test_database_connection():
    """Veritabanı bağlantısını test eder"""
    try:
        # Tabloları oluştur
        Base.metadata.create_all(bind=engine)
        print("✅ Veritabanı bağlantısı başarılı!")
        print("✅ Tablolar oluşturuldu!")
        return True
    except Exception as e:
        print(f"❌ Veritabanı bağlantı hatası: {e}")
        print("\n🔧 Çözüm önerileri:")
        print("1. PostgreSQL'in çalıştığından emin olun")
        print("2. config.py dosyasındaki bağlantı bilgilerini kontrol edin")
        print("3. Veritabanının oluşturulduğundan emin olun")
        return False

if __name__ == "__main__":
    print("Veritabanı Bağlantı Testi")
    print("=" * 30)
    test_database_connection() 