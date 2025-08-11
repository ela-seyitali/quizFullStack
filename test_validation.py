import requests
import json

def test_question_creation():
    print("🔍 Question Creation Validation Test")
    print("=" * 50)
    
    # Önce token al
    token_url = "http://127.0.0.1:8000/token"
    token_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        token_response = requests.post(token_url, data=token_data)
        if token_response.status_code != 200:
            print(f"❌ Token alma hatası: {token_response.status_code}")
            print(f"Response: {token_response.text}")
            return
        
        token = token_response.json()["access_token"]
        print(f"✅ Token alındı: {token[:20]}...")
        
        # Test 1: Minimal valid request
        print("\n🧪 Test 1: Minimal Valid Request")
        minimal_data = {
            "question_text": "Test soru?",
            "option_a": "A seçeneği",
            "option_b": "B seçeneği", 
            "option_c": "C seçeneği",
            "option_d": "D seçeneği",
            "correct_answer": "A",
            "category_id": 1
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            "http://127.0.0.1:8000/admin/questions/",
            json=minimal_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Minimal request başarılı!")
        else:
            print(f"❌ Hata: {response.text}")
            try:
                error_detail = response.json()
                print("🔍 Hata detayları:")
                for error in error_detail.get("detail", []):
                    print(f"  - Alan: {error.get('loc', [])}")
                    print(f"    Mesaj: {error.get('msg', '')}")
                    print(f"    Tip: {error.get('type', '')}")
            except:
                print(f"Raw response: {response.text}")
        
        # Test 2: Tüm alanlarla
        print("\n🧪 Test 2: Tüm Alanlarla")
        full_data = {
            "question_text": "Python hangi programlama paradigmasını destekler?",
            "option_a": "Sadece OOP",
            "option_b": "Sadece Fonksiyonel",
            "option_c": "Çoklu Paradigma", 
            "option_d": "Sadece Prosedürel",
            "correct_answer": "C",
            "explanation": "Python hem OOP hem fonksiyonel hem de prosedürel programlamayı destekler",
            "category_id": 3,
            "is_active": True
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/admin/questions/",
            json=full_data,
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Full request başarılı!")
        else:
            print(f"❌ Hata: {response.text}")
            try:
                error_detail = response.json()
                print("🔍 Hata detayları:")
                for error in error_detail.get("detail", []):
                    print(f"  - Alan: {error.get('loc', [])}")
                    print(f"    Mesaj: {error.get('msg', '')}")
                    print(f"    Tip: {error.get('type', '')}")
            except:
                print(f"Raw response: {response.text}")
                
    except Exception as e:
        print(f"❌ Genel hata: {e}")

if __name__ == "__main__":
    test_question_creation()
