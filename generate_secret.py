import secrets
import string

def generate_secret_key(length: int = 32) -> str:
    """Güvenli bir SECRET_KEY oluşturur"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Örnek .env dosyası oluşturur"""
    secret_key = generate_secret_key()
    
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/quiz_db

# Security Configuration
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ENVIRONMENT=development
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ .env dosyası oluşturuldu!")
        print(f"🔑 SECRET_KEY: {secret_key}")
        print("\n⚠️  ÖNEMLİ:")
        print("1. .env dosyasını düzenleyerek DATABASE_URL'deki şifrenizi güncelleyin")
        print("2. Bu dosyayı asla GitHub'a yüklemeyin")
        print("3. Production'da SECRET_KEY'yi değiştirin")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        print("\n📝 Manuel olarak .env dosyası oluşturun:")
        print("1. Proje klasöründe .env dosyası oluşturun")
        print("2. Aşağıdaki içeriği kopyalayın:")
        print("-" * 50)
        print(env_content)
        print("-" * 50)

if __name__ == "__main__":
    print("🔐 Güvenli .env Dosyası Oluşturucu")
    print("=" * 40)
    create_env_file() 