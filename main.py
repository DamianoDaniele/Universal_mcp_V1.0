# main.py
import ai_handler
#import readline # Opzionale, per migliore esperienza input da terminale (history, editing)

def main():
    """Loop principale dell'applicazione MCP."""
    print("--- Applicazione MCP Server Universale Locale ---")
    print("Digita 'quit' o 'exit' per uscire.")

    conversation_history = [] # Mantiene il contesto della conversazione

    while True:
        try:
            prompt = input("\nTu: ")
            if prompt.lower() in ['quit', 'exit']:
                print("Arrivederci!")
                break

            if not prompt:
                continue

            # Invia il prompt all'AI Handler, che gestirà anche le chiamate alle funzioni
            ai_response_text, updated_history = ai_handler.get_ai_response(prompt, conversation_history)

            # Aggiorna la cronologia per le interazioni future
            conversation_history = updated_history

            # Mostra la risposta finale all'utente
            print(f"\nGemini: {ai_response_text}")

        except EOFError: # Gestisce Ctrl+D
             print("\nArrivederci!")
             break
        except KeyboardInterrupt: # Gestisce Ctrl+C
            print("\nInterruzione rilevata. Uscita.")
            break
        except Exception as e:
            print(f"\n!!! Errore imprevisto nel loop principale: {e} !!!")
            # Potrebbe essere utile resettare la history o gestire l'errore in altro modo
            # conversation_history = [] # Opzione: resetta la conversazione in caso di errore grave


if __name__ == "__main__":
    main()