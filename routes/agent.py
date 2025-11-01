python
from pydantic import BaseModel
from typing import Optional, List

# Aggiungi questo modello
class ChatRequest(BaseModel):
    prompt: str
    use_tools: bool = False
    user_id: Optional[str] = "default"
    tools_list: Optional[List[str]] = None

# Modifica l'endpoint
@router.post("/chat")
async def chat_with_tools(
    request: ChatRequest,
    api_key: str = Depends(verify_api_key)
):
    try:
        prompt = request.prompt
        use_tools = request.use_tools
        user_id = request.user_id
        tools_list = request.tools_list

        if not prompt:
            raise HTTPException(status_code=400, detail="Campo 'prompt' mancante o vuoto")

        print(f"📩 Prompt ricevuto: {prompt}")
        print(f"🔧 Use tools: {use_tools}")
        if tools_list:
            print(f"🛠️  Tools list: {tools_list}")

        # Scegli tra chat semplice o con tool
        if use_tools:
            result = deepseek_manager.chat_with_tools(prompt, user_id, tools_list)
        else:
            result = deepseek_manager.simple_chat(prompt)

        # Gestisci errori
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Errore interno del server: {str(e)}"
        )