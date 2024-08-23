# Modular Pinecone YouTube API

This project is a modular API designed for managing a Pinecone knowledgebase and downloading YouTube transcripts. The project is implemented in Python using FastAPI and is structured into reusable modules for future extensions.

## Features

- **Pinecone Knowledgebase Management:**
  - List available indexes.
  - Upsert vectors into an index.
  - Query similar vectors.
  - Rerank query results using GPT-4.

- **YouTube Transcription Management:**
  - Download transcripts of individual YouTube videos.
  - Download transcripts of entire YouTube playlists.

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/modular-pinecone-youtube-api.git
    cd modular-pinecone-youtube-api
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Pinecone API Key:**

   Set your Pinecone API key in the `pinecone_module.py` file:

    ```python
    pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-east-1-gcp")
    ```

4. **Run the API server:**

    ```bash
    uvicorn main:app --reload
    ```

5. **Access the API documentation:**

   The API documentation will be available at `http://127.0.0.1:8000/docs`.

## API Endpoints

### Pinecone Knowledgebase Management

- **GET** `/indexes`: List available Pinecone indexes.
- **POST** `/vectors`: Upsert vectors to a Pinecone index.
- **POST** `/vectors/query`: Query similar vectors from a Pinecone index.
- **POST** `/vectors/rerank`: Rerank query results using GPT-4.

### YouTube Transcription Management

- **GET** `/youtube/download_transcript`: Download and transcribe a single YouTube video.
- **GET** `/youtube/download_playlist_transcripts`: Download and transcribe an entire YouTube playlist.

## Directory Structure

- `main.py`: The main entry point of the API.
- `pinecone_module.py`: Module handling Pinecone operations.
- `youtube_download_module.py`: Module handling YouTube download and transcription operations.

## License

This project is licensed under the MIT License.
