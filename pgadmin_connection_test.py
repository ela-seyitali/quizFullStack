#!/usr/bin/env python3
"""
pgAdmin connection test script
"""

import psycopg2
from app.core.config import settings

def test_pgadmin_connection():
    """Test connection with same credentials as pgAdmin"""
    try:
        print("🔍 Testing pgAdmin connection parameters...")
        print(f"📊 Database URL: {settings.DATABASE_URL}")
        
        # Parse connection string
        if "postgresql://" in settings.DATABASE_URL:
            # Extract components
            url_parts = settings.DATABASE_URL.replace("postgresql://", "").split("@")
            user_pass = url_parts[0].split(":")
            host_port_db = url_parts[1].split("/")
            host_port = host_port_db[0].split(":")
            
            username = user_pass[0]
            password = user_pass[1]
            host = host_port[0]
            port = host_port[1] if len(host_port) > 1 else "5432"
            database = host_port_db[1]
            
            print(f"👤 Username: {username}")
            print(f"🔒 Password: {'*' * len(password)}")
            print(f"🌐 Host: {host}")
            print(f"🔌 Port: {port}")
            print(f"🗄️ Database: {database}")
            
            # Test connection
            print("\n🔗 Testing connection...")
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password
            )
            
            print("✅ pgAdmin connection successful!")
            
            # Test cursor
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"📊 PostgreSQL Version: {version}")
            
            cursor.close()
            conn.close()
            
            return True
            
    except Exception as e:
        print(f"❌ pgAdmin connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 pgAdmin Connection Test")
    print("=" * 40)
    
    success = test_pgadmin_connection()
    
    if success:
        print("\n🎉 pgAdmin should work with these settings!")
        print("\n📋 pgAdmin Connection Settings:")
        print("Host: 127.0.0.1")
        print("Port: 5432")
        print("Database: quiz_db")
        print("Username: postgres")
        print("Password: [your_password]")
    else:
        print("\n🔧 Please check your pgAdmin configuration!")
