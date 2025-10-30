from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Callable
import functools

# Importa il decoratore e le funzioni di test
from modules.main.test_functions import logga_chiamata, esegui_test_completo

router = APIRouter(prefix="/api/v1", tags=["Agent"])

@router.get("/test-decoratore")
async def test_decoratore():
    """
    Test del decoratore logga_chiamata.
    Esegue le funzioni decorate e restituisce i risultati con log.
    """
    try:
        # Esegui il test completo che include le funzioni decorate
        risultati = esegui_test_completo()
        
        # Aggiungi un esempio di funzione decorata al volo
        @logga_chiamata
        def funzione_temporanea():
            return "Questa è una funzione temporanea decorata al volo!"
            
        # Aggiungi il risultato della funzione temporanea
        risultati["funzione_temporanea"] = funzione_temporanea()
        
        return {
            "status": "success",
            "message": "Test del decoratore completato con successo",
            "risultati": risultati
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore durante l'esecuzione del test del decoratore: {str(e)}"
        )