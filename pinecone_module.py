import os
from dotenv import load_dotenv
import pinecone
from sentence_transformers import SentenceTransformer
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))
index_name = os.getenv("PINECONE_INDEX_NAME", "default-index")
index = pinecone.Index(index_name)

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """Generate embedding for given text."""
    return model.encode(text).tolist()

def check_if_exists_in_pinecone(id):
    """Check if a vector with given id exists in Pinecone."""
    try:
        response = index.fetch([id])
        exists = id in response['vectors']
        logger.info(f"Check if exists in Pinecone for ID {id}: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking existence in Pinecone: {e}")
        raise

def embed_and_add_to_pinecone(id, vector, title):
    """Add a vector to Pinecone index."""
    try:
        index.upsert([(id, vector, {'title': title})])
        logger.info(f"Added vector to Pinecone with ID {id}")
    except Exception as e:
        logger.error(f"Error adding to Pinecone: {e}")
        raise

def rerank_results(query_vector, results):
    """Rerank results based on cosine similarity."""
    try:
        ranked_results = sorted(results, key=lambda x: cosine_similarity(query_vector, x[1]), reverse=True)
        logger.info("Results reranked based on cosine similarity.")
        return ranked_results
    except Exception as e:
        logger.error(f"Error during reranking: {e}")
        raise

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    if magnitude1 * magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)
