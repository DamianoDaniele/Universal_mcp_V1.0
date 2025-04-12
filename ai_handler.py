# ai_handler.py
import google.generativeai as genai
from config_manager import get_api_key
import file_manager # Importa per accedere alle definizioni delle funzioni
import web_browser  # Importa per accedere alle definizioni delle funzioni

# --- Configurazione dell'API Google Gemini ---
API_KEY = get_api_key('google')
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("API Key di Google non configurata. Le funzioni AI non saranno disponibili.")
    # Potresti voler sollevare un'eccezione o uscire

# --- Definizione degli Strumenti (Tools) per Gemini ---
# Gemini ha bisogno di una descrizione strutturata delle funzioni che può chiamare.
# Combiniamo le funzioni dai nostri moduli

# Descrizioni basate sulle docstring delle funzioni reali
tools = [
    # Strumenti da file_manager
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="create_file",
                description=file_manager.create_file.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'filename': genai.protos.Schema(type=genai.protos.Type.STRING, description="Il percorso del file da creare."),
                        'content': genai.protos.Schema(type=genai.protos.Type.STRING, description="Contenuto iniziale opzionale.")
                    },
                    required=['filename']
                )
            ),
            genai.protos.FunctionDeclaration(
                name="read_file",
                description=file_manager.read_file.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'filename': genai.protos.Schema(type=genai.protos.Type.STRING, description="Il percorso del file da leggere.")
                    },
                    required=['filename']
                )
            ),
            genai.protos.FunctionDeclaration(
                name="update_file",
                description=file_manager.update_file.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'filename': genai.protos.Schema(type=genai.protos.Type.STRING, description="Il percorso del file da aggiornare."),
                        'content': genai.protos.Schema(type=genai.protos.Type.STRING, description="Il nuovo contenuto."),
                        'mode': genai.protos.Schema(type=genai.protos.Type.STRING, description="Modalità: 'overwrite' o 'append'.")
                    },
                    required=['filename', 'content']
                )
            ),
            genai.protos.FunctionDeclaration(
                name="delete_file",
                description=file_manager.delete_file.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'filename': genai.protos.Schema(type=genai.protos.Type.STRING, description="Il percorso del file da cancellare.")
                    },
                    required=['filename']
                )
            ),
             genai.protos.FunctionDeclaration(
                name="list_files",
                description=file_manager.list_files.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'directory': genai.protos.Schema(type=genai.protos.Type.STRING, description="Directory da elencare (default '.')")
                    },
                    required=[] # directory è opzionale
                )
            ),
        ]
    ),
     # Strumenti da web_browser
     genai.protos.Tool(
        function_declarations=[
             genai.protos.FunctionDeclaration(
                name="search_web",
                description=web_browser.search_web.__doc__,
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        'query': genai.protos.Schema(type=genai.protos.Type.STRING, description="La query di ricerca."),
                        'num_results': genai.protos.Schema(type=genai.protos.Type.INTEGER, description="Numero di risultati (default 5).")
                    },
                    required=['query']
                )
            )
        ]
    )
]

# Combina le funzioni disponibili da tutti i moduli in un unico dizionario
ALL_AVAILABLE_FUNCTIONS = {
    **file_manager.AVAILABLE_FUNCTIONS,
    **web_browser.AVAILABLE_FUNCTIONS,
    # Aggiungi qui altri dizionari di funzioni da nuovi moduli
}

# Modello Gemini da utilizzare (scegline uno che supporti function calling)
MODEL_NAME = "gemini-2.5-pro-exp-03-25" # O "gemini-1.0-pro", "gemini-1.5-pro", #gemini-1.5-flash

def get_ai_response(prompt: str, history: list = None):
    """
    Invia il prompt all'AI (Gemini), gestisce il function calling e restituisce la risposta finale.

    Args:
        prompt (str): Il prompt dell'utente.
        history (list, optional): La cronologia della conversazione per mantenere il contesto.

    Returns:
        tuple: (risposta_testuale: str, nuova_cronologia: list)
               La risposta può essere il risultato diretto dell'AI o il risultato dell'esecuzione di una funzione.
    """
    if not API_KEY:
        return "Errore: API Key di Google non disponibile.", history or []

    try:
        model = genai.GenerativeModel(MODEL_NAME, tools=tools)
        chat = model.start_chat(history=history or [])

        print(">>> Invio prompt all'AI...")
        response = chat.send_message(prompt)
        print("<<< Risposta ricevuta dall'AI.")

        # Loop per gestire potenziali chiamate multiple di funzioni
        while response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            args = {key: value for key, value in function_call.args.items()}

            print(f"--- Richiesta chiamata funzione: {function_name}({args}) ---")

            if function_name in ALL_AVAILABLE_FUNCTIONS:
                # Esegui la funzione locale corrispondente
                function_to_call = ALL_AVAILABLE_FUNCTIONS[function_name]
                try:
                    # Chiamata sicura passando gli argomenti come keyword arguments
                    function_response = function_to_call(**args)
                    print(f"--- Risultato funzione: {function_response[:200]}... ---") # Log troncato
                except Exception as e:
                    print(f"!!! Errore durante l'esecuzione di {function_name}: {e} !!!")
                    function_response = f"Errore nell'esecuzione della funzione {function_name}: {e}"

                # Invia il risultato della funzione di nuovo all'AI
                print(">>> Invio risultato funzione all'AI...")
                response = chat.send_message(
                    genai.protos.Part(function_response=genai.protos.FunctionResponse(
                        name=function_name,
                        response={'result': function_response} # Struttura richiesta
                    )),
                )
                print("<<< Risposta ricevuta dall'AI post-funzione.")
            else:
                # Funzione richiesta dall'AI ma non definita localmente
                print(f"!!! Funzione '{function_name}' richiesta dall'AI ma non trovata localmente. Invio errore all'AI. !!!")
                response = chat.send_message(
                     genai.protos.Part(function_response=genai.protos.FunctionResponse(
                        name=function_name,
                        response={'error': f"Funzione '{function_name}' non disponibile."}
                    )),
                )

        # Dopo il loop (o se non c'erano function call), ottieni la risposta testuale finale
        final_text_response = response.candidates[0].content.parts[0].text if response.candidates[0].content.parts else "Nessuna risposta testuale dall'AI."
        return final_text_response, chat.history

    except Exception as e:
        print(f"!!! Errore durante l'interazione con l'API Gemini: {e} !!!")
        # Potresti voler vedere i dettagli dell'errore response.prompt_feedback
        # if 'response' in locals() and response.prompt_feedback:
        #    print(f"Prompt Feedback: {response.prompt_feedback}")
        return f"Si è verificato un errore durante la comunicazione con l'AI: {e}", history or []
