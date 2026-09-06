import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.connection import engine, Base, SessionLocal
from backend.app.curriculum.loader import seed_curriculum_and_questions
from backend.app.api import auth, curriculum, assessments, roadmap, ai, telemetry, supporting, assignments, upsc
from backend.app.api.supporting import admin_router

# Initialize DB tables
Base.metadata.create_all(bind=engine)

# Seed curriculum and question bank on startup
with SessionLocal() as db:
    seed_curriculum_and_questions(db)

app = FastAPI(
    title="Adaptive Student Intelligence & Roadmap Engine (JEE Main, NEET & UPSC Civil Services)",
    description="Offline-first, mathematically-grounded adaptive assessment, ML prediction, dynamic roadmap engine, official image-based benchmark testing, and UPSC Prelims/Mains evaluation.",
    version="1.3.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(curriculum.router, prefix="/api")
app.include_router(assessments.router, prefix="/api")
app.include_router(assignments.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(telemetry.router, prefix="/api")
app.include_router(upsc.router, prefix="/api")
app.include_router(supporting.router, prefix="/api")
app.include_router(admin_router, prefix="/api")

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

@app.get("/")
def root(request: Request):
    accept_header = request.headers.get("accept", "").lower()
    
    # If a browser requests HTML, serve index.html
    if "text/html" in accept_header:
        index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "index.html"))
        if os.path.exists(index_path):
            return FileResponse(index_path)

    # Otherwise return system status JSON (for API clients, tests, etc.)
    return {
        "status": "online",
        "service": "Adaptive Student Intelligence & Dynamic Roadmap Backend API",
        "version": "1.3.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_url": "/api/health"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "engine": "Adaptive Student Intelligence & Dynamic Roadmap Platform",
        "supported_exams": ["JEE", "NEET", "UPSC"],
        "models": ["MultiFactor_Mastery", "Ebbinghaus_Decay", "BKT_Knowledge_Tracing", "IRT_2PL", "NetworkX_DAG_Prerequisites"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
