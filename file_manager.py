# file_manager.py
import os

# --- Funzioni Strumento Definibili ---
# Queste funzioni saranno quelle che l'AI può richiedere di eseguire.
# Devono avere docstring chiare che ne spieghino l'uso e i parametri.

def create_file(filename: str, content: str = "") -> str:
    """
    Crea un nuovo file con il nome specificato e contenuto opzionale.
    Restituisce un messaggio di successo o errore.
    Args:
        filename (str): Il percorso completo o relativo del file da creare.
        content (str, optional): Il contenuto iniziale da scrivere nel file. Default "".
    Returns:
        str: Messaggio di risultato.
    """
    try:
        # Evita sovrascritture accidentali, l'AI dovrebbe chiamare update_file per questo
        if os.path.exists(filename):
            return f"Errore: Il file '{filename}' esiste già. Usa update_file per modificarlo."
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{filename}' creato con successo."
    except Exception as e:
        return f"Errore durante la creazione del file '{filename}': {e}"

def read_file(filename: str) -> str:
    """
    Legge il contenuto di un file esistente.
    Restituisce il contenuto del file o un messaggio di errore.
    Args:
        filename (str): Il percorso del file da leggere.
    Returns:
        str: Contenuto del file o messaggio di errore.
    """
    try:
        if not os.path.exists(filename):
            return f"Errore: Il file '{filename}' non trovato."
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        # Per file molto grandi, potresti voler restituire solo un'anteprima o un messaggio
        # return f"Contenuto del file '{filename}':\n{content[:1000]}" # Esempio con limite
        return content
    except Exception as e:
        return f"Errore durante la lettura del file '{filename}': {e}"

def update_file(filename: str, content: str, mode: str = 'overwrite') -> str:
    """
    Aggiorna un file esistente scrivendo nuovo contenuto o aggiungendolo.
    Restituisce un messaggio di successo o errore.
    Args:
        filename (str): Il percorso del file da aggiornare.
        content (str): Il contenuto da scrivere o aggiungere.
        mode (str, optional): 'overwrite' per sovrascrivere, 'append' per aggiungere. Default 'overwrite'.
    Returns:
        str: Messaggio di risultato.
    """
    try:
        write_mode = 'w' if mode == 'overwrite' else 'a'
        # Verifica se il file esiste prima di tentare di aprirlo in modalità append o write
        # 'w' crea il file se non esiste, 'a' anche.
        # Potrebbe essere utile verificare esplicitamente l'esistenza se la logica lo richiede.
        # if not os.path.exists(filename) and mode == 'append':
        #     return f"Errore: Impossibile aggiungere al file '{filename}' perchè non esiste."

        with open(filename, write_mode, encoding='utf-8') as f:
            f.write(content)
        action = "sovrascritto" if mode == 'overwrite' else "aggiornato (append)"
        return f"File '{filename}' {action} con successo."
    except Exception as e:
        return f"Errore durante l'aggiornamento del file '{filename}': {e}"

def delete_file(filename: str) -> str:
    """
    Cancella un file specificato.
    Restituisce un messaggio di successo o errore.
    Args:
        filename (str): Il percorso del file da cancellare.
    Returns:
        str: Messaggio di risultato.
    """
    try:
        if not os.path.exists(filename):
            return f"Errore: Impossibile cancellare, il file '{filename}' non trovato."
        os.remove(filename)
        return f"File '{filename}' cancellato con successo."
    except Exception as e:
        return f"Errore durante la cancellazione del file '{filename}': {e}"

def list_files(directory: str = ".") -> str:
    """
    Elenca i file e le directory nella directory specificata.
    Restituisce l'elenco o un messaggio di errore.
    Args:
        directory (str, optional): Il percorso della directory da elencare. Default '.'.
    Returns:
        str: Elenco di file/directory o messaggio di errore.
    """
    try:
        if not os.path.isdir(directory):
            return f"Errore: La directory '{directory}' non esiste o non è valida."
        items = os.listdir(directory)
        if not items:
            return f"La directory '{directory}' è vuota."
        return f"Contenuto di '{directory}':\n" + "\n".join(items)
    except Exception as e:
        return f"Errore durante l'elenco della directory '{directory}': {e}"

# Mappa dei nomi delle funzioni agli oggetti funzione reali per facilitare la chiamata
AVAILABLE_FUNCTIONS = {
    "create_file": create_file,
    "read_file": read_file,
    "update_file": update_file,
    "delete_file": delete_file,
    "list_files": list_files,
}