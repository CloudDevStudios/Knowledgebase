
import pinecone
import logging
from openai.embeddings_utils import get_embedding  # Assuming usage of OpenAI for embeddings

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
        # Actual embedding logic using OpenAI embeddings or another model
        with open(file, 'r') as f:
            content = f.read()
        vector = get_embedding(content)  # Replace with actual embedding logic
        index.upsert([(id, vector)])
        logging.info(f"Embedding and adding file to Pinecone with ID {id}")
    except Exception as e:
        logging.error(f"Error embedding and adding to Pinecone: {e}")
        raise

def rerank_results(query_vector, results):
    try:
        # Assuming results is a list of tuples (id, vector)
        ranked_results = sorted(results, key=lambda x: cosine_similarity(query_vector, x[1]), reverse=True)
        logging.info("Results reranked based on cosine similarity.")
        return ranked_results
    except Exception as e:
        logging.error(f"Error during reranking: {e}")
        raise

def cosine_similarity(vec1, vec2):
    return sum(x * y for x, y in zip(vec1, vec2)) / (sum(x**2 for x in vec1) ** 0.5 * sum(y**2 for y in vec2) ** 0.5)
