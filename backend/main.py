from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastApi.routes import api_router
import os
from dotenv import load_dotenv

load_dotenv()

#metadata
app = FastAPI(
    title="Prompt Engine API",
    description="AI-powered prompt engineering coach and refiner with intelligent frameworks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Including API routes
app.include_router(api_router)

# Enabling CORS for frontend access
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/health")
async def health_check():
    """Check if API and critical services are responsive"""
    from agents.coach_agent import DB_URI
    import psycopg
    
    health = {
        "status": "up",
        "database": "unknown",
        "environment": {
            "GROQ_API_KEY": "set" if os.environ.get("GROQ_API_KEY") else "missing",
            "DATABASE_URL": "set" if os.environ.get("DATABASE_URL") else "missing",
            "TAVILY_API_KEY": "set" if os.environ.get("TAVILY_API_KEY") else "missing"
        }
    }
    
    # Check Database
    try:
        conn = psycopg.connect(DB_URI)
        conn.close()
        health["database"] = "connected"
    except Exception as e:
        health["status"] = "partially_down"
        health["database"] = f"error: {str(e)}"
        
    return health

@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Prompt Engine API",
        "version": "1.0.0",
        "services": {
            "coaching": "/coaching/",
            "refiner": "/refiner/",
            "health": "/health"
        }
    }
