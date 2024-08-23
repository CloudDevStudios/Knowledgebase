from fastapi import FastAPI, HTTPException, BackgroundTasks
import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Configure logger
logger.add("logs/api.log", rotation="500 MB")

app = FastAPI()

@app.get("/indexes")
async def list_indexes():
    try:
        indexes = ["chosen"]  # Replace with dynamic listing if needed
        logger.info("Listed Pinecone indexes successfully.")
        return {"indexes": indexes}
    except Exception as e:
        logger.error(f"Error listing indexes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
