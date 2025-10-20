# Decoratore per logging
def logga_chiamata(func):
    def wrapper():
        print(f"▶️ INIZIO {func.__name__}")
        risultato = func()
        print(f"⏹️  FINE {func.__name__} → {risultato}")
        return risultato
    return wrapper

# Funzioni con decoratore
@logga_chiamata
def saluta():
    return "Ciao Mondo!"

@logga_chiamata
def somma_semplice():
    return 5 + 3

# Funzione principale di test
def esegui_test_completo():
    """Esegue tutte le funzioni decorate e restituisce risultati con log"""
    print("\n" + "="*50)
    print("🧪 TEST COMPLETO FUNZIONI DECORATE")
    print("="*50)
    
    risultati = {
        "saluto": saluta(),
        "somma": somma_semplice()
    }
    
    print("="*50)
    print("✅ TEST COMPLETATO")
    print("="*50)
    
    return risultati
