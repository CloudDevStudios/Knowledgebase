from yt_dlp import YoutubeDL
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_transcripts(video_url, transcript_language, output_dir, output_file_name):
    """Download transcript for a YouTube video."""
    try:
        ydl_opts = {
            'writesubtitles': True,
            'subtitleslangs': [transcript_language],
            'skip_download': True,
            'outtmpl': os.path.join(output_dir, f"{output_file_name}.%(ext)s"),
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            logger.info(f"Downloaded transcript for video {video_url}")
    except Exception as e:
        logger.error(f"Error downloading transcript for video {video_url}: {e}")
        raise

def get_youtube_playlist_count(playlist_url):
    """Get the number of videos in a YouTube playlist."""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            count = len(info['entries'])
            logger.info(f"Total videos in playlist {playlist_url}: {count}")
            return count
    except Exception as e:
        logger.error(f"Error getting playlist count for {playlist_url}: {e}")
        raise

def get_youtube_playlist_items(playlist_url):
    """Get the list of video titles in a YouTube playlist."""
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            videos = [entry['title'] for entry in info['entries']]
            logger.info(f"Retrieved {len(videos)} video titles from playlist {playlist_url}")
            return videos
    except Exception as e:
        logger.error(f"Error getting playlist items for {playlist_url}: {e}")
        raise
