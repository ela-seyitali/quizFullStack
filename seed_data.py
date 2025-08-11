from sqlalchemy.orm import Session
from database import get_db
from crud import create_question, get_category
from schemas import QuestionCreate

def seed_sample_questions():
    """Örnek sorular ekler"""
    db = next(get_db())
    
    try:
        # Kategorileri al
        ml_category = get_category(db, 1)  # Machine Learning
        ai_category = get_category(db, 2)  # Artificial Intelligence
        prog_category = get_category(db, 3)  # Programming
        cyber_category = get_category(db, 4)  # Cyber Security
        
        if not all([ml_category, ai_category, prog_category, cyber_category]):
            print("Kategoriler bulunamadı! Önce uygulamayı çalıştırın.")
            return
        
        # Machine Learning soruları
        ml_questions = [
            {
                "question_text": "Hangi algoritma sınıflandırma problemleri için kullanılır?",
                "option_a": "Linear Regression",
                "option_b": "Logistic Regression",
                "option_c": "K-means Clustering",
                "option_d": "Principal Component Analysis",
                "correct_answer": "B",
                "explanation": "Logistic Regression sınıflandırma problemleri için kullanılır.",
                "category_id": 1
            },
            {
                "question_text": "Overfitting nedir?",
                "option_a": "Modelin eğitim verilerini ezberlemesi",
                "option_b": "Modelin yetersiz öğrenmesi",
                "option_c": "Veri setinin küçük olması",
                "option_d": "Modelin çok hızlı çalışması",
                "correct_answer": "A",
                "explanation": "Overfitting, modelin eğitim verilerini ezberleyip genelleme yapamamasıdır.",
                "category_id": 1
            },
            {
                "question_text": "Cross-validation'ın amacı nedir?",
                "option_a": "Modeli hızlandırmak",
                "option_b": "Model performansını değerlendirmek",
                "option_c": "Veri setini küçültmek",
                "option_d": "Modeli basitleştirmek",
                "correct_answer": "B",
                "explanation": "Cross-validation model performansını değerlendirmek için kullanılır.",
                "category_id": 1
            }
        ]
        
        # Artificial Intelligence soruları
        ai_questions = [
            {
                "question_text": "Narrow AI nedir?",
                "option_a": "Genel amaçlı yapay zeka",
                "option_b": "Belirli bir görev için tasarlanmış AI",
                "option_c": "İnsan benzeri AI",
                "option_d": "Süper AI",
                "correct_answer": "B",
                "explanation": "Narrow AI belirli bir görev için tasarlanmış yapay zekadır.",
                "category_id": 2
            },
            {
                "question_text": "Turing Testi neyi ölçer?",
                "option_a": "Bilgisayar hızını",
                "option_b": "AI'nın insan benzeri davranışını",
                "option_c": "Algoritma karmaşıklığını",
                "option_d": "Veri işleme kapasitesini",
                "correct_answer": "B",
                "explanation": "Turing Testi AI'nın insan benzeri davranış sergileyip sergilemediğini ölçer.",
                "category_id": 2
            },
            {
                "question_text": "Expert System nedir?",
                "option_a": "Uzman sistem",
                "option_b": "Öğrenme sistemi",
                "option_c": "Veri işleme sistemi",
                "option_d": "Görüntü işleme sistemi",
                "correct_answer": "A",
                "explanation": "Expert System belirli bir alanda uzmanlaşmış yapay zeka sistemidir.",
                "category_id": 2
            }
        ]
        
        # Programming soruları
        prog_questions = [
            {
                "question_text": "Python'da 'self' parametresi ne anlama gelir?",
                "option_a": "Sınıf adı",
                "option_b": "Instance referansı",
                "option_c": "Fonksiyon adı",
                "option_d": "Değişken adı",
                "correct_answer": "B",
                "explanation": "self parametresi sınıf instance'ının referansını temsil eder.",
                "category_id": 3
            },
            {
                "question_text": "Git'te 'merge' komutu ne yapar?",
                "option_a": "Dosya siler",
                "option_b": "Branch'leri birleştirir",
                "option_c": "Commit oluşturur",
                "option_d": "Repository klonlar",
                "correct_answer": "B",
                "explanation": "merge komutu farklı branch'leri birleştirmek için kullanılır.",
                "category_id": 3
            },
            {
                "question_text": "REST API nedir?",
                "option_a": "Web servisi standardı",
                "option_b": "Veritabanı türü",
                "option_c": "Programlama dili",
                "option_d": "İşletim sistemi",
                "correct_answer": "A",
                "explanation": "REST API web servisleri için kullanılan bir standarttır.",
                "category_id": 3
            }
        ]
        
        # Cyber Security soruları
        cyber_questions = [
            {
                "question_text": "SQL Injection nedir?",
                "option_a": "Veritabanı saldırısı",
                "option_b": "Şifre kırma",
                "option_c": "Virüs türü",
                "option_d": "Firewall türü",
                "correct_answer": "A",
                "explanation": "SQL Injection veritabanlarına zararlı SQL kodları enjekte etme saldırısıdır.",
                "category_id": 4
            },
            {
                "question_text": "HTTPS protokolü ne sağlar?",
                "option_a": "Hız artışı",
                "option_b": "Güvenli iletişim",
                "option_c": "Dosya sıkıştırma",
                "option_d": "Veri sıkıştırma",
                "correct_answer": "B",
                "explanation": "HTTPS güvenli iletişim sağlar ve verileri şifreler.",
                "category_id": 4
            },
            {
                "question_text": "Phishing saldırısı nedir?",
                "option_a": "Fiziksel saldırı",
                "option_b": "Sosyal mühendislik saldırısı",
                "option_c": "DDoS saldırısı",
                "option_d": "Virüs saldırısı",
                "correct_answer": "B",
                "explanation": "Phishing kullanıcıları kandırarak hassas bilgileri elde etme saldırısıdır.",
                "category_id": 4
            }
        ]
        
        # Tüm soruları ekle
        all_questions = ml_questions + ai_questions + prog_questions + cyber_questions
        
        for question_data in all_questions:
            question = QuestionCreate(**question_data)
            create_question(db=db, question=question)
        
        print(f"Toplam {len(all_questions)} soru başarıyla eklendi!")
        print(f"Machine Learning: {len(ml_questions)} soru")
        print(f"Artificial Intelligence: {len(ai_questions)} soru")
        print(f"Programming: {len(prog_questions)} soru")
        print(f"Cyber Security: {len(cyber_questions)} soru")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Örnek sorular ekleme aracı")
    print("=" * 40)
    seed_sample_questions() 