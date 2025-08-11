# Quiz API - FastAPI ve PostgreSQL ile Quiz Uygulaması

Bu proje, FastAPI ve PostgreSQL kullanarak geliştirilmiş kapsamlı bir quiz uygulamasıdır. Hem web hem de mobil uygulamalar için API endpoint'leri sağlar.

## Özellikler

- **Kullanıcı Yönetimi**: Kayıt, giriş ve JWT token tabanlı kimlik doğrulama
- **Admin Paneli**: Quiz soruları ve kategorileri yönetimi
- **Quiz Sistemi**: Kategorilere göre quiz çözme ve skor takibi
- **İstatistikler**: Kullanıcı performans analizi
- **4 Ana Kategori**: Machine Learning, Artificial Intelligence, Programming, Cyber Security

## Teknolojiler

- **Backend**: FastAPI
- **Veritabanı**: PostgreSQL
- **ORM**: SQLAlchemy
- **Kimlik Doğrulama**: JWT
- **Şifreleme**: bcrypt

## Kurulum

### 1. Gereksinimler

- Python 3.8+
- PostgreSQL
- pip

### 2. Veritabanı Kurulumu

PostgreSQL'de yeni bir veritabanı oluşturun:

```sql
CREATE DATABASE quiz_db;
```

### 3. Proje Kurulumu

```bash
# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Güvenli .env dosyası oluşturun
python generate_secret.py

# .env dosyasını düzenleyin
# DATABASE_URL'deki şifrenizi güncelleyin
```

### 4. Güvenlik Konfigürasyonu

#### .env Dosyası Oluşturma

Proje güvenliği için `.env` dosyası kullanılır:

```bash
# Otomatik .env oluşturma
python generate_secret.py
```

Veya manuel olarak `.env` dosyası oluşturun:

```env
# Database Configuration
DATABASE_URL=postgresql://your_password@localhost:5432/quiz_db

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ENVIRONMENT=development
```

#### Önemli Güvenlik Notları:

1. **`.env` dosyasını asla GitHub'a yüklemeyin**
2. **Production'da SECRET_KEY'yi değiştirin**
3. **Veritabanı şifrenizi güvenli tutun**
4. **`.env` dosyası `.gitignore`'da listelenmiştir**

### 5. Uygulamayı Çalıştırma

```bash
python main.py
```

veya

```bash
uvicorn main:app --reload
```

Uygulama http://localhost:8000 adresinde çalışacaktır.

## API Endpoint'leri

### Kimlik Doğrulama

- `POST /token` - Kullanıcı girişi
- `POST /register` - Yeni kullanıcı kaydı

### Kategoriler

- `GET /categories/` - Tüm kategorileri listele
- `GET /categories/{category_id}` - Belirli kategoriyi getir
- `POST /categories/` - Yeni kategori oluştur (Admin)

### Sorular (Admin)

- `GET /questions/` - Tüm soruları listele
- `GET /questions/{question_id}` - Belirli soruyu getir
- `POST /questions/` - Yeni soru oluştur
- `PUT /questions/{question_id}` - Soru güncelle
- `DELETE /questions/{question_id}` - Soru sil

### Quiz

- `POST /quiz/start/{category_id}` - Quiz başlat
- `GET /quiz/questions/{category_id}` - Quiz sorularını getir
- `POST /quiz/submit/{session_id}` - Quiz'i tamamla
- `GET /quiz/history/` - Quiz geçmişi
- `GET /quiz/statistics/` - Quiz istatistikleri

## Admin Kullanıcı Oluşturma

İlk admin kullanıcısını oluşturmak için:

```bash
python create_admin.py
```

## Örnek Veriler Ekleme

```bash
python seed_data.py
```

## Veritabanı Şeması

### Categories
- id (Primary Key)
- name (Unique)
- description

### Questions
- id (Primary Key)
- question_text
- option_a, option_b, option_c, option_d
- correct_answer
- explanation
- category_id (Foreign Key)
- is_active
- created_at, updated_at

### Users
- id (Primary Key)
- username (Unique)
- email (Unique)
- hashed_password
- is_admin
- created_at

### QuizSessions
- id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key)
- score
- total_questions
- completed_at

## API Dokümantasyonu

Uygulama çalıştıktan sonra şu adreslerde API dokümantasyonuna erişebilirsiniz:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Mobil Uygulama Entegrasyonu

Bu API, mobil uygulamalar için de kullanılabilir. Tüm endpoint'ler JSON formatında veri alır ve döndürür. JWT token tabanlı kimlik doğrulama sistemi mobil uygulamalar için uygundur.

## Güvenlik

- JWT token tabanlı kimlik doğrulama
- bcrypt ile şifre hashleme
- Admin yetki kontrolü
- SQL injection koruması (SQLAlchemy ORM)
- Environment variables ile güvenli konfigürasyon
- .env dosyası ile hassas bilgilerin korunması

## Geliştirme

### Yeni Özellik Ekleme

1. `models.py` - Veritabanı modellerini ekleyin
2. `schemas.py` - Pydantic şemalarını ekleyin
3. `crud.py` - CRUD işlemlerini ekleyin
4. `main.py` - API endpoint'lerini ekleyin

### Test

```bash
# Veritabanı bağlantısını test edin
python test_db.py

# Örnek veriler ekleyin
python seed_data.py
```

## Production Deployment

Production ortamında:

1. **SECRET_KEY'yi değiştirin**
2. **DEBUG=False yapın**
3. **Güçlü veritabanı şifresi kullanın**
4. **HTTPS kullanın**
5. **Environment variables'ları sunucu konfigürasyonunda ayarlayın**

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 