from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
import os
from dotenv import load_dotenv
from loguru import logger
from pinecone_module import check_if_exists_in_pinecone, embed_and_add_to_pinecone, rerank_results, cosine_similarity, index as pinecone_index
import youtube_download_module
import re

# Load environment variables
load_dotenv()

# Configure logger
logger.add("logs/api.log", rotation="500 MB")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class VectorModel(BaseModel):
    id: str
    vector: List[float]

class QueryModel(BaseModel):
    vector: List[float]
    top_k: int = Field(default=10, ge=1, le=100)

# Helper Functions
def is_valid_youtube_url(url: str) -> bool:
    """Checks if a URL is a valid YouTube video or playlist URL."""
    youtube_regex = re.compile(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(?:playlist\?list=)?([a-zA-Z0-9_-]+)")
    return bool(youtube_regex.match(url))

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/indexes")
async def list_indexes():
    """Lists available Pinecone indexes."""
    try:
        indexes = ["chosen"]  # Replace with dynamic listing if needed
        logger.info("Listed Pinecone indexes successfully.")
        return {"indexes": indexes}
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/vectors")
async def upsert_vectors(vectors: List[VectorModel]):
    """Upserts vectors to the Pinecone index."""
    try:
        upserted_vectors = []
        for v in vectors:
            # Check if vector already exists
            if not check_if_exists_in_pinecone(v.id):
                embed_and_add_to_pinecone(v.id, v.vector, "Sample Title")
                upserted_vectors.append((v.id, v.vector))
            else:
                logger.info(f"Vector with ID {v.id} already exists. Skipping.")

        logger.info(f"Upserted vectors: {upserted_vectors}")
        return {"message": "Vectors upserted successfully.", "upserted_count": len(upserted_vectors)}
    except Exception as e:
        logger.error(f"Error upserting vectors: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/vectors/query")
async def query_vectors(query: QueryModel):
    """Queries the Pinecone index for similar vectors."""
    try:
        results = pinecone_index.query(
            vector=query.vector,
            top_k=query.top_k,
            include_values=True,
            include_metadata=True
        ).to_dict()['matches']

        result_tuples = [(result['id'], result['values']) for result in results]
        reranked_results = rerank_results(query.vector, result_tuples)

        logger.info(f"Queried and reranked vectors: {reranked_results}")
        return {"results": reranked_results}
    except Exception as e:
        logger.error(f"Error querying vectors: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/youtube/download_transcript")
async def download_transcript(
    video_url: str = Query(..., description="The URL of the YouTube video"),
    output_dir: str = "transcripts",
    output_file_name: str = "transcript",
    transcript_language: str = "en"
):
    """Downloads a transcript for a YouTube video."""
    try:
        if not is_valid_youtube_url(video_url):
            raise ValueError("Invalid YouTube URL provided.")

        youtube_download_module.download_transcripts(video_url, transcript_language, output_dir, output_file_name)
        transcript_path = os.path.join(output_dir, f"{output_file_name}.{transcript_language}.vtt")

        if not os.path.exists(transcript_path):
            raise FileNotFoundError(f"Transcript file not found at: {transcript_path}")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
        logger.info(f"Downloaded transcript for video {video_url}")
        return {"transcript": transcript}
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Error downloading transcript: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error downloading transcript for video {video_url}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/youtube/download_playlist_transcripts")
async def download_playlist_transcripts(
    playlist_url: str = Query(..., description="The URL of the YouTube playlist"),
    background_tasks: BackgroundTasks
):
    """Initiates background task to download transcripts for all videos in a YouTube playlist."""
    try:
        if not is_valid_youtube_url(playlist_url):
            raise ValueError("Invalid YouTube playlist URL provided.")

        video_count = youtube_download_module.get_youtube_playlist_count(playlist_url)
        background_tasks.add_task(download_playlist_transcripts_task, playlist_url)
        
        return {"message": f"Started downloading {video_count} transcripts from the playlist. This may take a while."}
    except ValueError as e:
        logger.error(f"Error initiating playlist transcript download: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error initiating playlist transcript download for {playlist_url}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def download_playlist_transcripts_task(playlist_url: str):
    """Background task to download transcripts for all videos in a playlist."""
    try:
        video_titles = youtube_download_module.get_youtube_playlist_items(playlist_url)
        for title in video_titles:
            file_name = title.replace(" ", "_").replace("/", "_")
            youtube_download_module.download_transcripts(playlist_url, "en", "transcripts", file_name)
        logger.info(f"Completed downloading transcripts for playlist {playlist_url}")
    except Exception as e:
        logger.error(f"Error in background task for downloading playlist transcripts: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
