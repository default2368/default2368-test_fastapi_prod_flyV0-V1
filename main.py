import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = FastAPI(
    title="MCP System API",
    description="Sistema integrato FastAPI + MCP Server",
    version="2.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ENDPOINTS PRINCIPALI SEMPLIFICATI =====

@app.get("/", include_in_schema=False)
async def root():
    """Redirect alla documentazione API"""
    return RedirectResponse(url="/docs")

@app.get("/welcome")
async def welcome():
    """Endpoint di benvenuto"""
    return {
        "message": "Benvenuto nel sistema Fast APi",
        "version": os.getenv("VERSION", "0.0.0"),
        "description": "Sistema integrato FastAPI + MCP Server"
    }