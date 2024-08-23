import pinecone

# Initialisiere Pinecone
pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-east-1-gcp")
index = pinecone.Index("chosen")

def check_if_exists_in_pinecone(id):
    # Implementiere Logik zur Überprüfung, ob ID bereits in Pinecone vorhanden ist
    # Dies ist ein Platzhalter - passe die Logik je nach API an
    return False

def embed_and_add_to_pinecone(file, id, title):
    # Implementiere die Einbettungs- und Hinzufügungslogik hier
    print(f"Embedding {file} to Pinecone with ID {id}")
    # Hier die tatsächliche Pinecone-API-Logik implementieren
