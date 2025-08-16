"""
Authentication endpoints.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.user import create_user, get_user_by_username, get_user_by_email
from app.schemas.user import User, UserCreate
from app.schemas.token import Token
from app.core.security import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", tags=["auth"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Yeni kullanıcı kaydı oluşturur.
    
    - **username**: Benzersiz kullanıcı adı (3-50 karakter)
    - **email**: Geçerli email adresi
    - **password**: Şifre (en az 6 karakter)
    - **is_admin**: Admin yetkisi (true/false)
    
    Başarılı kayıt sonrası kullanıcı oluşturulur.
    """
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = create_user(db=db, user=user)
    
    return {
        "message": "✅ Kullanıcı başarıyla oluşturuldu!",
        "user": created_user,
        "note": "Şimdi /token endpoint'i ile giriş yapabilirsiniz."
    }

@router.post("/token", response_model=Token, tags=["auth"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Kullanıcı girişi ve JWT token oluşturma.
    
    - **username**: Kullanıcı adı
    - **password**: Şifre
    
    Başarılı giriş sonrası JWT access token döner.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
