import pinecone
import logging

# Initialize logging
logging.basicConfig(filename='pinecone_api.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize Pinecone
pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-east-1-gcp")
index = pinecone.Index("chosen")

def check_if_exists_in_pinecone(id):
    try:
        response = index.fetch([id])
        exists = id in response['vectors']
        logging.info(f"Check if exists in Pinecone for ID {id}: {exists}")
        return exists
    except Exception as e:
        logging.error(f"Error checking existence in Pinecone: {e}")
        raise

def embed_and_add_to_pinecone(file, id, title):
    try:
        # Placeholder for embedding logic - typically you would use a model like OpenAI's embeddings
        vector = [0.0] * 512  # Replace with actual embedding logic
        index.upsert([(id, vector)])
        logging.info(f"Embedding and adding file to Pinecone with ID {id}")
    except Exception as e:
        logging.error(f"Error embedding and adding to Pinecone: {e}")
        raise
