
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from loguru import logger
from pinecone_module import check_if_exists_in_pinecone, embed_and_add_to_pinecone, rerank_results

# Load environment variables
load_dotenv()

# Configure logger
logger.add("logs/api.log", rotation="500 MB")

# Initialize FastAPI app
app = FastAPI()

class VectorModel(BaseModel):
    id: str
    vector: List[float]

class QueryModel(BaseModel):
    vector: List[float]
    top_k: int = 10

@app.get("/indexes")
async def list_indexes():
    try:
        indexes = ["chosen"]  # Replace with dynamic listing if needed
        logger.info("Listed Pinecone indexes successfully.")
        return {"indexes": indexes}
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/vectors")
async def upsert_vectors(vectors: List[VectorModel]):
    try:
        # Here we assume vectors is a list of dicts with 'id' and 'vector'
        upserted_vectors = [(v.id, v.vector) for v in vectors]
        embed_and_add_to_pinecone("placeholder_file.txt", vectors[0].id, "Sample Title")
        logger.info(f"Upserted vectors: {upserted_vectors}")
        return {"message": "Vectors upserted successfully."}
    except Exception as e:
        logger.error(f"Error upserting vectors: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/vectors/query")
async def query_vectors(query: QueryModel):
    try:
        # Example usage of querying vectors
        result = [{"id": "some-id", "vector": query.vector}]  # Placeholder for actual querying logic
        reranked_results = rerank_results(query.vector, result)
        logger.info(f"Queried and reranked vectors: {reranked_results}")
        return {"results": reranked_results}
    except Exception as e:
        logger.error(f"Error querying vectors: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/youtube/download_transcript")
async def download_transcript(video_url: str = Query(..., description="The URL of the YouTube video")):
    try:
        # Placeholder logic for downloading transcript
        logger.info(f"Downloaded transcript for video {video_url}")
        return {"transcript": "Transcript text"}
    except Exception as e:
        logger.error(f"Error downloading transcript for video {video_url}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/youtube/download_playlist_transcripts")
async def download_playlist_transcripts(playlist_url: str = Query(..., description="The URL of the YouTube playlist"), background_tasks: BackgroundTasks):
    try:
        transcripts = {}
        # Placeholder logic for downloading playlist transcripts
        logger.info(f"Downloaded transcripts for playlist {playlist_url}")
        return {"transcripts": transcripts}
    except Exception as e:
        logger.error(f"Error downloading playlist transcripts for {playlist_url}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
