from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import asyncio

from modules.mcp import mcp_client

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/test")
async def mcp_test():
    """Endpoint di test per il server MCP"""
    try:
        # Testa tutti i componenti MCP
        health_check = await mcp_client.health_check()
        tools_list = await mcp_client.list_tools()
        
        # Esegue alcuni test di esempio
        test_results = []
        
        # Test 1: Server info
        server_info = await mcp_client.execute_tool("get_server_info", {})
        test_results.append({
            "test": "get_server_info",
            "result": server_info
        })
        
        # Test 2: Calcolo
        calculation = await mcp_client.execute_tool(
            "calculate_operation", 
            {"operation": "sum", "numbers": [1, 2, 3, 4, 5]}
        )
        test_results.append({
            "test": "calculate_operation",
            "result": calculation
        })
        
        # Test 3: Formattazione testo
        text_format = await mcp_client.execute_tool(
            "format_text",
            {"text": "Hello MCP World!", "style": "uppercase"}
        )
        test_results.append({
            "test": "format_text", 
            "result": text_format
        })
        
        return {
            "status": "success",
            "health_check": health_check,
            "available_tools": tools_list,
            "test_results": test_results,
            "message": "Test MCP completato con successo!"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante il test MCP: {str(e)}")

@router.get("/tools")
async def list_mcp_tools():
    """Lista tutti i tool MCP disponibili"""
    try:
        result = await mcp_client.list_tools()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nel recupero tools: {str(e)}")

@router.post("/tools/{tool_name}")
async def execute_mcp_tool(tool_name: str, parameters: Dict[str, Any] = None):
    """Esegue un tool MCP specifico"""
    try:
        if parameters is None:
            parameters = {}
            
        result = await mcp_client.execute_tool(tool_name, parameters)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("error", "Errore sconosciuto"))
            
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore nell'esecuzione del tool: {str(e)}")

@router.get("/health")
async def mcp_health():
    """Health check del server MCP"""
    try:
        result = await mcp_client.health_check()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore health check: {str(e)}")

@router.get("/")
async def mcp_root():
    """Endpoint root per MCP"""
    tools = await mcp_client.list_tools()
    health = await mcp_client.health_check()
    
    return {
        "message": "MCP Router attivo",
        "health": health,
        "available_tools": tools.get("tools", []),
        "endpoints": {
            "test": "/mcp/test",
            "health": "/mcp/health",
            "tools": "/mcp/tools",
            "execute_tool": "/mcp/tools/{tool_name} (POST)"
        }
    }
