import requests

def get_token():
    url = "http://127.0.0.1:8000/token"
    
    # Form data (username ve password) - DÜZELTİLDİ!
    data = {
        "username": "admin",  # admin_user değil, admin
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Token başarıyla alındı!")
            print(f"Token Type: {token_data['token_type']}")
            print(f"Access Token: {token_data['access_token']}")
            print("\n🔑 Bu token'ı Swagger UI'da kullanın!")
            return token_data['access_token']
        else:
            print(f"❌ Hata: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Bağlantı hatası: {e}")
        return None

if __name__ == "__main__":
    print("🔑 Admin Token Alma Scripti")
    print("=" * 40)
    token = get_token()
