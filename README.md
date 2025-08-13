# 🎯 Quiz FullStack API

Modern ve ölçeklenebilir quiz uygulaması API'si. FastAPI, PostgreSQL ve JWT authentication ile geliştirilmiştir.

## 🚀 Özellikler

- **🔐 JWT Authentication** - Güvenli kullanıcı girişi ve token yönetimi
- **👑 Role-Based Access Control** - Admin ve normal kullanıcı yetkileri
- **📚 Kategori Yönetimi** - Quiz kategorileri oluşturma ve düzenleme
- **❓ Soru Yönetimi** - Çoktan seçmeli sorular ekleme ve düzenleme
- **🎯 Quiz Sistemi** - Dinamik quiz oluşturma ve skor takibi
- **📊 İstatistikler** - Kullanıcı performans analizi
- **🌐 RESTful API** - Modern ve standart API tasarımı
- **📖 Swagger UI** - Otomatik API dokümantasyonu

## 🏗️ Proje Mimarisi

```
quizFullStack/
├── app/                          # Ana uygulama
│   ├── api/v1/endpoints/         # API endpoint'leri
│   │   ├── auth.py              # Kimlik doğrulama
│   │   ├── categories.py        # Kategori işlemleri
│   │   ├── questions.py         # Soru işlemleri
│   │   └── quiz.py              # Quiz işlemleri
│   ├── core/                     # Çekirdek bileşenler
│   │   ├── config.py            # Konfigürasyon
│   │   ├── database.py          # Veritabanı
│   │   └── security.py          # Güvenlik
│   ├── crud/                     # CRUD işlemleri
│   │   ├── user.py              # Kullanıcı CRUD
│   │   ├── category.py          # Kategori CRUD
│   │   ├── question.py          # Soru CRUD
│   │   └── quiz_session.py      # Quiz session CRUD
│   ├── models/                   # Veritabanı modelleri
│   │   ├── user.py              # Kullanıcı modeli
│   │   ├── category.py          # Kategori modeli
│   │   ├── question.py          # Soru modeli
│   │   └── quiz_session.py      # Quiz session modeli
│   ├── schemas/                  # Pydantic şemaları
│   │   ├── user.py              # Kullanıcı şemaları
│   │   ├── category.py          # Kategori şemaları
│   │   ├── question.py          # Soru şemaları
│   │   ├── quiz_session.py      # Quiz session şemaları
│   │   └── token.py             # Token şemaları
│   └── main.py                   # Ana FastAPI uygulaması
├── scripts/                      # Yardımcı scriptler
│   ├── init_db.py               # Veritabanı başlatma
│   ├── create_user.py           # Kullanıcı oluşturma
│   ├── create_category.py       # Kategori oluşturma
│   ├── create_question.py       # Soru oluşturma
│   ├── create_quiz_sessions.py  # Quiz session oluşturma
│   ├── list_users.py            # Kullanıcı listeleme
│   └── list_quiz_sessions.py    # Quiz session listeleme
├── tests/                        # Test dosyaları
├── main.py                       # Uygulama giriş noktası
├── requirements.txt              # Bağımlılıklar
├── .env                          # Ortam değişkenleri
└── README.md                     # Proje dokümantasyonu
```

## 🛠️ Teknolojiler

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: SHA256
- **API Documentation**: Swagger UI / OpenAPI
- **Validation**: Pydantic v2
- **Server**: Uvicorn (ASGI)

## 📋 Gereksinimler

- Python 3.8+
- PostgreSQL 12+
- pip

## 🚀 Kurulum

### 1. Repository'yi klonlayın
```bash
git clone <repository-url>
cd quizFullStack
```

### 2. Virtual environment oluşturun
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# veya
source .venv/bin/activate  # Linux/Mac
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment variables ayarlayın
`.env` dosyası oluşturun:
```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/quiz_db

# Security Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ENVIRONMENT=development
```

### 5. Veritabanını başlatın
```bash
python scripts/init_db.py
```

### 6. Uygulamayı çalıştırın
```bash
python main.py
```

## 🌐 API Endpoints

### 🔐 Authentication
- `POST /api/v1/token` - Kullanıcı girişi
- `POST /api/v1/register` - Yeni kullanıcı kaydı

### 📚 Categories
- `POST /api/v1/admin/categories/` - Yeni kategori oluştur (Admin)
- `GET /api/v1/admin/categories/` - Tüm kategorileri listele (Admin)
- `GET /api/v1/categories/{category_id}` - Kategori detayı
- `GET /api/v1/quiz/categories/` - Quiz için kategoriler

### ❓ Questions
- `POST /api/v1/admin/questions/` - Yeni soru oluştur (Admin)
- `GET /api/v1/admin/questions/` - Tüm soruları listele (Admin)
- `GET /api/v1/admin/questions/{question_id}` - Soru detayı (Admin)
- `PUT /api/v1/admin/questions/{question_id}` - Soru güncelle (Admin)
- `DELETE /api/v1/admin/questions/{question_id}` - Soru sil (Admin)
- `GET /api/v1/quiz/questions/{category_id}` - Quiz için sorular

### 🎯 Quiz
- `POST /api/v1/quiz/start/{category_id}` - Quiz başlat
- `POST /api/v1/quiz/submit/{session_id}` - Quiz cevaplarını gönder
- `GET /api/v1/quiz/history/` - Quiz geçmişi
- `GET /api/v1/quiz/statistics/` - Quiz istatistikleri

## 🔧 Kullanım

### Swagger UI
API dokümantasyonu için: `http://127.0.0.1:8000/docs`

### Admin Kullanıcı
Varsayılan admin hesabı:
- **Username**: `admin`
- **Password**: `admin123`

### Yeni Kullanıcı Oluşturma
```bash
python scripts/create_user.py
```

### Yeni Kategori Oluşturma
```bash
python scripts/create_category.py
```

### Yeni Soru Oluşturma
```bash
python scripts/create_question.py
```

## 📊 Veritabanı Şeması

### Users Tablosu
- `id`: Primary Key
- `username`: Benzersiz kullanıcı adı
- `email`: Benzersiz email
- `hashed_password`: Şifrelenmiş şifre
- `is_admin`: Admin yetkisi
- `created_at`: Oluşturulma tarihi

### Categories Tablosu
- `id`: Primary Key
- `name`: Kategori adı
- `description`: Kategori açıklaması

### Questions Tablosu
- `id`: Primary Key
- `question_text`: Soru metni
- `option_a`, `option_b`, `option_c`, `option_d`: Seçenekler
- `correct_answer`: Doğru cevap (A/B/C/D)
- `explanation`: Açıklama
- `category_id`: Kategori referansı
- `is_active`: Aktif durumu
- `created_at`, `updated_at`: Tarih bilgileri

### Quiz_Sessions Tablosu
- `id`: Primary Key
- `user_id`: Kullanıcı referansı
- `category_id`: Kategori referansı
- `score`: Doğru cevap sayısı
- `total_questions`: Toplam soru sayısı
- `started_at`: Başlangıç zamanı
- `completed_at`: Bitiş zamanı

## 🔒 Güvenlik

- **JWT Token**: 30 dakika geçerli
- **Password Hashing**: SHA256 ile şifreleme
- **Role-Based Access**: Admin ve normal kullanıcı ayrımı
- **Input Validation**: Pydantic ile veri doğrulama

## 🧪 Test

```bash
# Uygulama testi
python -c "from app.main import app; print('✅ Import successful')"

# Veritabanı testi
python scripts/init_db.py
```

## 📝 Geliştirme

### Yeni Endpoint Ekleme
1. `app/api/v1/endpoints/` altında yeni dosya oluştur
2. Router tanımla
3. `app/main.py`'de router'ı dahil et

### Yeni Model Ekleme
1. `app/models/` altında model tanımla
2. `app/schemas/` altında schema oluştur
3. `app/crud/` altında CRUD işlemleri ekle

## 🚀 Deployment

### Production
```bash
# Environment variables
export ENVIRONMENT=production
export DEBUG=False

# Uvicorn ile çalıştır
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker (Gelecek)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

- **Husam** - Quiz FullStack API

## 📞 İletişim

- **GitHub**: [@husam](https://github.com/husam)
- **Email**: husam@example.com

## 🙏 Teşekkürler

- FastAPI ekibine
- SQLAlchemy geliştiricilerine
- PostgreSQL topluluğuna

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! 