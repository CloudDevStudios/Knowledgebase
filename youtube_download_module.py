import os
import logging
from yt_dlp import YoutubeDL

# Initialize logging
logging.basicConfig(filename='youtube_api.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def download_transcripts(video_url, transcript_language, output_dir, output_file_name):
    try:
        ydl_opts = {
            'writesubtitles': True,
            'subtitleslangs': [transcript_language],
            'skip_download': True,
            'outtmpl': os.path.join(output_dir, f"{output_file_name}.%(ext)s"),
            'cookiesfrombrowser': ('chrome',),
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            logging.info(f"Downloaded transcript for video {video_url}")
    except Exception as e:
        logging.error(f"Error downloading transcript for video {video_url}: {e}")
        raise

def get_youtube_playlist_count(playlist_url):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            count = len(info['entries'])
            logging.info(f"Total videos in playlist {playlist_url}: {count}")
            return count
    except Exception as e:
        logging.error(f"Error getting playlist count for {playlist_url}: {e}")
        raise

def get_youtube_playlist_items(playlist_url):
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            videos = [entry['title'] for entry in info['entries']]
            logging.info(f"Video titles in playlist {playlist_url}: {videos}")
            return videos
    except Exception as e:
        logging.error(f"Error getting playlist items for {playlist_url}: {e}")
        raise
