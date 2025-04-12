# web_browser.py
import requests
from bs4 import BeautifulSoup
import json

# --- Funzione Strumento Definibile ---

def search_web(query: str, num_results: int = 5) -> str:
    """
    Esegue una ricerca web utilizzando Google e restituisce i primi risultati.
    ATTENZIONE: Lo scraping diretto di Google può essere inaffidabile e violare i ToS.
              Considera API ufficiali o servizi terzi per uso intensivo/produzione.
    Args:
        query (str): La stringa di ricerca.
        num_results (int, optional): Numero massimo di risultati da restituire. Default 5.
    Returns:
        str: Stringa formattata con i risultati (titolo, link, snippet) o messaggio di errore.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Prepara l'URL per la ricerca Google
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"

        response = requests.get(search_url, headers=headers)
        response.raise_for_status() # Solleva eccezione per status code non 2xx

        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        # Trova i blocchi dei risultati (questi selettori potrebbero cambiare!)
        # È necessario ispezionare l'HTML di Google per trovare i selettori corretti
        # Questo è un esempio e probabilmente dovrà essere aggiornato
        for g in soup.find_all('div', class_='g'): # Classe comune per i risultati organici
            # Estrai titolo, link e snippet (potrebbero servire selettori più specifici)
            title_tag = g.find('h3')
            link_tag = g.find('a')
            snippet_tag = g.find('div', class_='VwiC3b') # Esempio di classe per snippet

            title = title_tag.text if title_tag else "N/A"
            link = link_tag['href'] if link_tag else "N/A"
            snippet = snippet_tag.text if snippet_tag else "N/A"

            if link != "N/A" and not link.startswith("/"): # Ignora link interni di Google
                 results.append({
                     "title": title,
                     "link": link,
                     "snippet": snippet
                 })
                 if len(results) >= num_results:
                     break # Raggiunto il numero desiderato

        if not results:
            return f"Nessun risultato trovato per '{query}' (o impossibile estrarli)."

        # Formatta l'output per l'AI/utente
        output = f"Risultati ricerca web per '{query}':\n\n"
        for i, res in enumerate(results):
             output += f"{i+1}. {res['title']}\n   Link: {res['link']}\n   Snippet: {res['snippet']}\n\n"
        return output.strip()

    except requests.exceptions.RequestException as e:
        return f"Errore di rete durante la ricerca web: {e}"
    except Exception as e:
        return f"Errore imprevisto durante l'analisi dei risultati di ricerca: {e}"

# Mappa per la chiamata
AVAILABLE_FUNCTIONS = {
    "search_web": search_web,
}