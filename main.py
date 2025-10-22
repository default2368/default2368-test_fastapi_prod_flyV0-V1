import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from modules.test import esegui_test_completo
from routes.mcp_router import router as mcp_router

# Carica le variabili d'ambiente dal file .env
load_dotenv()

app = FastAPI(
    title="MCP System API",
    description="Sistema integrato FastAPI + MCP Server con DeepSeek",
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

# Includi il router MCP
app.include_router(mcp_router)

# ===== ENDPOINTS PRINCIPALI AGGIORNATI =====

@app.get("/", include_in_schema=False)
async def root():
    """Redirect alla documentazione API"""
    return RedirectResponse(url="/docs")

@app.get("/welcome")
async def welcome():
    """Endpoint di benvenuto aggiornato"""
    return {
        "message": "Benvenuto nel sistema FastAPI + MCP Server",
        "version": os.getenv("VERSION", "2.0.0"),
        "description": "Sistema integrato FastAPI + MCP Server con DeepSeek",
        "features": [
            "API REST completa",
            "Integrazione MCP Server", 
            "Tool per calcoli matematici",
            "Tool per formattazione testo",
            "Monitoraggio sistema",
            "Documentazione automatica"
        ]
    }

@app.get("/test")
async def test_endpoint():
    """Testa le funzioni decorate locali"""
    risultati = esegui_test_completo()
    
    return {
        "status": "success",
        "risultati": risultati,
        "message": "Controlla i log del server per vedere il decoratore in azione!"
    }

@app.get("/status")
async def system_status():
    """Restituisce lo stato completo del sistema"""
    from modules.mcp import mcp_client
    
    # Ottieni lo stato MCP
    mcp_health = await mcp_client.health_check()
    tools_list = await mcp_client.list_tools()
    
    return {
        "system": "online",
        "version": os.getenv("VERSION", "2.0.0"),
        "mcp_integration": mcp_health,
        "available_mcp_tools": tools_list.get("tools", []),
        "endpoints_available": [
            "/welcome",
            "/status", 
            "/test",
            "/mcp/",
            "/mcp/test",
            "/mcp/health",
            "/mcp/tools",
            "/docs"
        ]
    }

@app.get("/mcp/quick-test")
async def mcp_quick_test():
    """Test rapido delle funzionalità MCP più comuni"""
    from modules.mcp import mcp_client
    
    test_results = []
    
    # Test 1: Informazioni server
    server_info = await mcp_client.execute_tool("get_server_info", {})
    test_results.append({
        "tool": "get_server_info",
        "status": server_info.get("status"),
        "data": server_info.get("result", {})
    })
    
    # Test 2: Calcolo rapido
    calculation = await mcp_client.execute_tool(
        "calculate_operation", 
        {"operation": "sum", "numbers": [10, 20, 30]}
    )
    test_results.append({
        "tool": "calculate_operation",
        "status": calculation.get("status"),
        "data": calculation.get("result", {})
    })
    
    # Test 3: Formattazione testo
    text_result = await mcp_client.execute_tool(
        "format_text",
        {"text": "quick mcp test", "style": "uppercase"}
    )
    test_results.append({
        "tool": "format_text",
        "status": text_result.get("status"),
        "data": text_result.get("result", {})
    })
    
    return {
        "test": "quick_mcp_test",
        "results": test_results,
        "summary": f"{len([r for r in test_results if r.get('status') == 'success'])}/{len(test_results)} test passed"
    }

@app.post("/calculate")
async def calculate_numbers(operation: str, numbers: list):
    """Endpoint semplificato per calcoli matematici usando MCP"""
    from modules.mcp import mcp_client
    
    result = await mcp_client.execute_tool(
        "calculate_operation",
        {"operation": operation, "numbers": numbers}
    )
    
    if result.get("status") == "error":
        return {
            "status": "error",
            "error": result.get("error", "Errore sconosciuto")
        }
    
    return {
        "status": "success",
        "operation": operation,
        "numbers": numbers,
        "result": result.get("result", {}).get("result"),
        "timestamp": result.get("result", {}).get("timestamp")
    }

@app.post("/format")
async def format_text_endpoint(text: str, style: str = "uppercase"):
    """Endpoint semplificato per formattazione testo usando MCP"""
    from modules.mcp import mcp_client
    
    result = await mcp_client.execute_tool(
        "format_text",
        {"text": text, "style": style}
    )
    
    if result.get("status") == "error":
        return {
            "status": "error",
            "error": result.get("error", "Errore sconosciuto")
        }
    
    return {
        "status": "success",
        "original_text": text,
        "formatted_text": result.get("result", {}).get("formatted"),
        "style": style,
        "length": result.get("result", {}).get("length"),
        "timestamp": result.get("result", {}).get("timestamp")
    }

@app.get("/server-info")
async def get_server_info():
    """Endpoint per informazioni del server MCP"""
    from modules.mcp import mcp_client
    
    result = await mcp_client.execute_tool("get_server_info", {})
    
    if result.get("status") == "error":
        return {
            "status": "error",
            "error": result.get("error", "Errore sconosciuto")
        }
    
    return {
        "status": "success",
        "server_info": result.get("result", {})
    }

# ===== HEALTH CHECK E MONITORING =====

@app.get("/health")
async def health_check():
    """Health check completo del sistema"""
    from modules.mcp import mcp_client
    
    try:
        # Verifica MCP
        mcp_status = await mcp_client.health_check()
        
        return {
            "status": "healthy",
            "fastapi": "running",
            "mcp_integration": mcp_status.get("status", "unknown"),
            "timestamp": "2024-01-15T10:30:00Z"  # In produzione usa datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "fastapi": "running",
            "mcp_integration": "error",
            "error": str(e),
            "timestamp": "2024-01-15T10:30:00Z"
        }

# ===== INFO PER SVILUPPATORI =====

@app.get("/info")
async def developer_info():
    """Informazioni per sviluppatori"""
    return {
        "project": "FastAPI + MCP Server Integration",
        "version": "2.0.0",
        "description": "Sistema che integra FastAPI con Model Context Protocol server",
        "architecture": {
            "fastapi": "Server REST principale",
            "mcp_server": "Server per tool e funzionalità AI",
            "integration": "Comunicazione via SSE/HTTP"
        },
        "endpoints": {
            "root": "/",
            "documentation": "/docs",
            "system_status": "/status",
            "health_check": "/health",
            "mcp_integration": "/mcp/",
            "quick_test": "/mcp/quick-test",
            "tools": "/mcp/tools"
        },
        "mcp_tools_available": [
            "get_server_info",
            "calculate_operation",
            "format_text", 
            "get_system_status"
        ]
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
