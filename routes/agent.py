from fastapi import APIRouter, HTTPException, Header, Depends
import json
import os
from typing import Optional

from modules.main.deepseek import deepseek_manager

router = APIRouter(prefix="/api/v1", tags=["Agent"])

# Middleware per verificare la chiave API
async def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    expected_key = os.getenv("DEEPSEEK_API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="API key non configurata sul server")
    
    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="API key non valida")
    return x_api_key

@router.post("/chat")
async def chat_with_tools(
    prompt: str,
    use_tools: bool = False,
    user_id: Optional[str] = "default",
    api_key: str = Depends(verify_api_key)
):
    """
    Endpoint per chat con DeepSeek
    """
    try:
        if not prompt:
            raise HTTPException(status_code=400, detail="Campo 'prompt' mancante o vuoto")

        # Log per debug
        print(f"Prompt ricevuto: {prompt}")

        # Scegli tra chat semplice o con tool
        if use_tools:
            result = deepseek_manager.chat_with_tools(prompt, user_id)
        else:
            result = deepseek_manager.simple_chat(prompt)

        # Gestisci errori
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore interno del server: {str(e)}"
        )

@router.get("/deepseek-status")
async def deepseek_status():
    """
    Verifica lo stato della connessione DeepSeek
    """
    result = deepseek_manager.test_connection()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return result