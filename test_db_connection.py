#!/usr/bin/env python3
"""
Database connection test script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine
from sqlalchemy import text

def test_database_connection():
    """Test database connection"""
    try:
        print("🔍 Testing database connection...")
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Test database version
            version_result = conn.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]
            print(f"📊 PostgreSQL Version: {version}")
            
            # Test quiz_db database
            db_result = conn.execute(text("SELECT current_database()"))
            current_db = db_result.fetchone()[0]
            print(f"🗄️ Current Database: {current_db}")
            
            # Test tables
            tables_result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in tables_result.fetchall()]
            print(f"📋 Available Tables: {tables}")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Database Connection Test")
    print("=" * 40)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database is working correctly!")
    else:
        print("\n🔧 Please check your PostgreSQL configuration!")
