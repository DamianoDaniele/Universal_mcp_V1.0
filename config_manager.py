# config_manager.py
import os
from dotenv import load_dotenv, find_dotenv


def load_config():
    """Carica le configurazioni dal file .env."""
    load_dotenv(dotenv_path=find_dotenv(filename="enviorement.env"))

    config = {
        'google_api_key': os.getenv('GOOGLE_API_KEY'),
        # Aggiungi qui altre chiavi caricate da .env
    }
    if not config['google_api_key']:
        print("Attenzione: GOOGLE_API_KEY non trovata nel file .env.")
        # Potresti voler gestire questo caso in modo più robusto (es. uscire o chiedere all'utente)
    return config

# Carica la configurazione all'importazione del modulo
CONFIG = load_config()

def get_api_key(service_name='google'):
    """Restituisce la API key per il servizio specificato."""
    if service_name == 'google':
        return CONFIG.get('google_api_key')
    # Aggiungi logica per altre API key
    return None
