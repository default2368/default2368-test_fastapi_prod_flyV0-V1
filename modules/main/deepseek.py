import os
import requests
from openai import OpenAI
from composio import Composio
from composio_openai import OpenAIProvider
from typing import Dict, Any, Optional

class DeepSeekManager:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.composio_api_key = os.getenv("COMPOSIO_API_KEY")
        
        # Inizializza client DeepSeek
        self.deepseek_client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        ) if self.api_key else None
        
        # Inizializza client Composio (opzionale)
        self.composio_client = Composio(
            api_key=self.composio_api_key,
            runtime=OpenAIProvider()
        ) if self.composio_api_key else None
    
    def is_configured(self) -> bool:
        """Verifica se DeepSeek è configurato correttamente"""
        return self.api_key is not None and self.deepseek_client is not None
    
    def simple_chat(self, message: str) -> Dict[str, Any]:
        """
        Chat semplice con DeepSeek senza tool
        """
        if not self.is_configured():
            return {"error": "DeepSeek non configurato. Imposta DEEPSEEK_API_KEY"}
        
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": "Sei un assistente utile. Rispondi in italiano."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=1000,
                temperature=0.7,
                stream=False
            )
            
            return {
                "response": response.choices[0].message.content,
                "model": "deepseek-chat",
                "usage": response.usage.dict() if response.usage else None
            }
            
        except Exception as e:
            return {"error": f"Errore DeepSeek: {str(e)}"}
    
    def chat_with_tools(self, message: str, user_id: str = "default") -> Dict[str, Any]:
        """
        Chat con DeepSeek utilizzando tool MCP tramite Composio
        """
        if not self.is_configured():
            return {"error": "DeepSeek non configurato"}
        
        if not self.composio_client:
            return {"error": "Composio non configurato"}
        
        try:
            # Recupera i tool MCP da Composio
            tools = self.composio_client.tools.get(
                user_id=user_id,
                tools=[
                    "get_server_info",
                    "calculate_operation",
                    "format_text",
                    "check_remote_health",
                    "get_weather"
                ]
            )
            
            # Chiama DeepSeek con i tool
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                tools=tools,
                messages=[
                    {
                        "role": "system",
                        "content": "Sei un assistente utile che ha accesso a vari tool. Usali quando appropriato."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=1000,
                temperature=0.7,
                stream=False
            )
            
            # Gestisci le chiamate ai tool
            result = self.composio_client.provider.handle_tool_calls(
                response=response,
                user_id=user_id
            )
            
            # Estrai la risposta finale
            if hasattr(result, 'choices') and result.choices:
                message_obj = result.choices[0].message
                response_text = message_obj.content or "Nessuna risposta di testo"
                tools_used = []
                
                if hasattr(message_obj, 'tool_calls') and message_obj.tool_calls:
                    tools_used = [tool.function.name for tool in message_obj.tool_calls]
                
                return {
                    "response": response_text,
                    "tools_used": tools_used,
                    "model": "deepseek-chat"
                }
            else:
                return {
                    "response": str(result),
                    "tools_used": [],
                    "model": "deepseek-chat"
                }
                
        except Exception as e:
            return {"error": f"Errore nella chat con tool: {str(e)}"}

    def test_connection(self) -> Dict[str, Any]:
        """
        Test della connessione a DeepSeek
        """
        if not self.is_configured():
            return {"status": "error", "message": "DeepSeek non configurato"}
        
        try:
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Rispondi solo con 'OK'"}],
                max_tokens=10,
                stream=False
            )
            
            return {
                "status": "success",
                "message": "Connessione a DeepSeek riuscita",
                "response": response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Errore di connessione: {str(e)}"
            }

# Istanza globale
deepseek_manager = DeepSeekManager()