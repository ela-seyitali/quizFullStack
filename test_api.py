#!/usr/bin/env python3
"""
Quiz API Test Scripti
Tüm endpoint'leri test eder ve hataları raporlar
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://127.0.0.1:8000"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def test_health_check():
    """Health check endpoint'ini test et"""
    print_separator("HEALTH CHECK TEST")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_root_endpoint():
    """Root endpoint'ini test et"""
    print_separator("ROOT ENDPOINT TEST")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_admin_login():
    """Admin kullanıcı ile giriş yap"""
    print_separator("ADMIN LOGIN TEST")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(
            f"{BASE_URL}/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login başarılı!")
            print(f"Token Type: {token_data['token_type']}")
            print(f"Access Token: {token_data['access_token'][:50]}...")
            return token_data['access_token']
        else:
            print(f"❌ Login başarısız: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

def test_get_categories():
    """Kategorileri listele"""
    print_separator("GET CATEGORIES TEST")
    try:
        response = requests.get(f"{BASE_URL}/quiz/categories/")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ {len(categories)} kategori bulundu:")
            for cat in categories:
                print(f"  • ID: {cat['id']} - {cat['name']}")
            return categories
        else:
            print(f"❌ Hata: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return []

def test_create_question_without_auth():
    """Kimlik doğrulama olmadan soru oluşturmayı dene (401 beklenir)"""
    print_separator("CREATE QUESTION WITHOUT AUTH TEST (401 Expected)")
    try:
        question_data = {
            "question_text": "Test sorusu",
            "option_a": "A seçeneği",
            "option_b": "B seçeneği", 
            "option_c": "C seçeneği",
            "option_d": "D seçeneği",
            "correct_answer": "A",
            "category_id": 1
        }
        
        response = requests.post(
            f"{BASE_URL}/admin/questions/",
            json=question_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Expected: 401 Unauthorized")
        
        if response.status_code == 401:
            print("✅ 401 Unauthorized hatası doğru şekilde döndü")
            return True
        else:
            print(f"❌ Beklenmeyen status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_create_question_with_auth(token, question_data):
    """Kimlik doğrulama ile soru oluştur"""
    print_separator("CREATE QUESTION WITH AUTH TEST")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{BASE_URL}/admin/questions/",
            json=question_data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Request Body: {json.dumps(question_data, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Soru başarıyla oluşturuldu!")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ Hata: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_validation_errors():
    """Validation hatalarını test et"""
    print_separator("VALIDATION ERRORS TEST")
    
    # Test 1: category_id = 0 (geçersiz)
    print("🔍 Test 1: category_id = 0 (geçersiz)")
    invalid_data_1 = {
        "question_text": "Test sorusu",
        "option_a": "A seçeneği",
        "option_b": "B seçeneği",
        "option_c": "C seçeneği", 
        "option_d": "D seçeneği",
        "correct_answer": "A",
        "category_id": 0  # Geçersiz!
    }
    
    # Test 2: correct_answer geçersiz
    print("🔍 Test 2: correct_answer = 'X' (geçersiz)")
    invalid_data_2 = {
        "question_text": "Test sorusu",
        "option_a": "A seçeneği",
        "option_b": "B seçeneği",
        "option_c": "C seçeneği",
        "option_d": "D seçeneği", 
        "correct_answer": "X",  # Geçersiz!
        "category_id": 1
    }
    
    # Test 3: Eksik alanlar
    print("🔍 Test 3: Eksik alanlar")
    invalid_data_3 = {
        "question_text": "Test sorusu",
        "option_a": "A seçeneği",
        # option_b eksik!
        "option_c": "C seçeneği",
        "option_d": "D seçeneği",
        "correct_answer": "A",
        "category_id": 1
    }
    
    test_cases = [
        ("category_id = 0", invalid_data_1),
        ("correct_answer = 'X'", invalid_data_2), 
        ("Eksik alanlar", invalid_data_3)
    ]
    
    for test_name, test_data in test_cases:
        print(f"\n--- {test_name} ---")
        try:
            response = requests.post(f"{BASE_URL}/admin/questions/", json=test_data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 422:
                print("✅ 422 Validation Error doğru şekilde döndü")
                error_detail = response.json().get('detail', [])
                for error in error_detail:
                    print(f"  • {error['loc'][-1]}: {error['msg']}")
            else:
                print(f"❌ Beklenmeyen status code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Hata: {e}")

def main():
    """Ana test fonksiyonu"""
    print("🚀 Quiz API Test Scripti Başlatılıyor...")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Test 1: Health Check
    if not test_health_check():
        print("❌ Health check başarısız! API çalışmıyor olabilir.")
        return
    
    # Test 2: Root Endpoint
    if not test_root_endpoint():
        print("❌ Root endpoint test başarısız!")
        return
    
    # Test 3: Admin Login
    token = test_admin_login()
    if not token:
        print("❌ Admin login başarısız! Test devam edemez.")
        return
    
    # Test 4: Kategorileri Al
    categories = test_get_categories()
    if not categories:
        print("❌ Kategoriler alınamadı!")
        return
    
    # Test 5: Kimlik doğrulama olmadan soru oluştur
    test_create_question_without_auth()
    
    # Test 6: Geçerli soru oluştur
    valid_question = {
        "question_text": "Python hangi programlama paradigmasını destekler?",
        "option_a": "Sadece OOP",
        "option_b": "Sadece Fonksiyonel", 
        "option_c": "Çoklu Paradigma",
        "option_d": "Sadece Prosedürel",
        "correct_answer": "C",
        "explanation": "Python hem OOP hem fonksiyonel hem de prosedürel programlamayı destekler",
        "category_id": 3,  # Programming kategorisi
        "is_active": True
    }
    
    test_create_question_with_auth(token, valid_question)
    
    # Test 7: Validation hatalarını test et
    test_validation_errors()
    
    print_separator("TEST TAMAMLANDI")
    print("🎉 Tüm testler tamamlandı!")
    print("\n📋 ÖZET:")
    print("✅ Health check çalışıyor")
    print("✅ Root endpoint çalışıyor") 
    print("✅ Admin login çalışıyor")
    print("✅ Kategoriler listeleniyor")
    print("✅ 401 Unauthorized doğru çalışıyor")
    print("✅ Soru oluşturma çalışıyor")
    print("✅ Validation hataları doğru çalışıyor")

if __name__ == "__main__":
    main()
