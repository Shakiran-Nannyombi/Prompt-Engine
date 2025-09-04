from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.fastApi.routes import api_router

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",  # Alternative localhost
        "http://localhost:3000",   # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Prompt Engine API",
        "version": "1.0.0",
        "services": {
            "coaching": "/coaching/",
            "refiner": "/refiner/"
        }
    }
