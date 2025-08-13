"""
Main FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.endpoints import auth, categories, questions, quiz

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "token",
                    "scopes": {}
                }
            }
        },
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add security to admin endpoints
    for path in openapi_schema["paths"]:
        if path.startswith("/admin/"):
            for method in openapi_schema["paths"][path]:
                if method in ["get", "post", "put", "delete"]:
                    openapi_schema["paths"][path][method]["security"] = [
                        {"OAuth2PasswordBearer": []},
                        {"BearerAuth": []}
                    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(questions.router, prefix=settings.API_V1_STR)
app.include_router(quiz.router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/", tags=["default"])
async def root():
    return {
        "message": "🎉 Quiz API başarıyla çalışıyor! 🎉",
        "status": "success",
        "version": settings.VERSION,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "api_v1": settings.API_V1_STR,
            "auth": {
                "register": f"{settings.API_V1_STR}/register",
                "login": f"{settings.API_V1_STR}/token"
            }
        },
        "description": "Bu API, quiz uygulaması için geliştirilmiştir. Kullanım için /docs endpoint'ini ziyaret edin."
    }

# Health check endpoint
@app.get("/health", tags=["default"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Quiz API çalışıyor ve sağlıklı!",
        "timestamp": "2024-01-01T00:00:00Z"
    }
