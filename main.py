"""
Quiz API - Main Entry Point
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting Quiz API...")
    print("📊 Database: PostgreSQL (quiz_db)")
    print("🌐 Server: http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
