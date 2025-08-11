from sqlalchemy.orm import Session
from database import get_db
from crud import create_user, get_user_by_username
from schemas import UserCreate

def create_admin_user(username: str, email: str, password: str):
    """Admin kullanıcısı oluşturur"""
    db = next(get_db())
    
    try:
        # Kullanıcının var olup olmadığını kontrol et
        existing_user = get_user_by_username(db, username)
        if existing_user:
            print(f"Kullanıcı '{username}' zaten mevcut!")
            return
        
        # Yeni kullanıcı oluştur
        user_data = UserCreate(username=username, email=email, password=password)
        new_user = create_user(db=db, user=user_data)
        
        # Admin yetkisi ver
        new_user.is_admin = True
        db.commit()
        
        print(f"Admin kullanıcısı '{username}' başarıyla oluşturuldu!")
        print(f"Email: {email}")
        print(f"Admin yetkisi: Evet")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Admin kullanıcısı oluşturma aracı")
    print("=" * 40)
    
    username = input("Kullanıcı adı: ")
    email = input("Email: ")
    password = input("Şifre: ")
    
    create_admin_user(username, email, password) 