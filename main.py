from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routes.agent import router as agent_router

app = FastAPI(
    title="Test Decorator API",
    description="API di test per il decoratore logga_chiamata",
    version="1.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Includi il router
app.include_router(agent_router)

# ===== ENDPOINTS PRINCIPALI =====

@app.get("/", include_in_schema=False)
async def root():
    """Redirect alla documentazione API"""
    return RedirectResponse(url="/docs")

@app.get("/status")
async def system_status():
    """Restituisce lo stato del sistema"""
    # Verifica lo spazio su disco
    import shutil
    total, used, free = shutil.disk_usage("/")
    
    return {
        "status": "operational",
        "version": "1.0.0",
        "system": {
            "disk_space": {
                "total_gb": round(total / (2**30), 2),
                "used_gb": round(used / (2**30), 2),
                "free_gb": round(free / (2**30), 2),
                "free_percent": round((free / total) * 100, 2)
            }
        },
        "endpoints": [
            "/status",
            "/api/v1/test-decoratore"
        ]
    }

# ===== HEALTH CHECK =====

@app.get("/health")
async def health_check():
    """Health check del sistema"""
    import platform
    import psutil
    from datetime import datetime
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "os": platform.system(),
            "python_version": platform.python_version(),
            "cpu_usage_percent": psutil.cpu_percent(),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
