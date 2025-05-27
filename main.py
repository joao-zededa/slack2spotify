import os
import re
import logging
import threading
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Slack configuration
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SPOTIFY_PLAYLIST_ID = os.getenv('SPOTIFY_PLAYLIST_ID')

# Initialize clients
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Spotify OAuth scope
SPOTIFY_SCOPE = 'playlist-modify-public playlist-modify-private'

# Initialize Spotify client
spotify_auth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
)

class YouTubeExtractor:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractaudio': False,
            'audioformat': 'mp3',
        }
    
    def extract_song_info(self, url):
        """Extract song information from YouTube URL"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', '')
                uploader = info.get('uploader', '')
                
                # Try to parse artist and song from title
                artist, song = self.parse_title(title)
                
                return {
                    'title': title,
                    'artist': artist,
                    'song': song,
                    'uploader': uploader,
                    'url': url
                }
        except Exception as e:
            logger.error(f"Error extracting info from {url}: {e}")
            return None
    
    def parse_title(self, title):
        """Parse artist and song name from YouTube title"""
        # Common patterns for music videos
        patterns = [
            r'^(.+?)\s*[-–—]\s*(.+?)(?:\s*\(.*\))?(?:\s*\[.*\])?$',  # Artist - Song
            r'^(.+?)\s*[:|]\s*(.+?)(?:\s*\(.*\))?(?:\s*\[.*\])?$',   # Artist : Song
            r'^(.+?)\s*"(.+?)"',  # Artist "Song"
            r'^(.+?)\s*[\'\'](.+?)[\'\']',  # Artist 'Song'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, title, re.IGNORECASE)
            if match:
                artist = match.group(1).strip()
                song = match.group(2).strip()
                return artist, song
        
        # If no pattern matches, return the full title as song
        return '', title

class SpotifyManager:
    def __init__(self):
        self.sp = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Spotify"""
        try:
            token_info = spotify_auth.get_cached_token()
            if not token_info:
                logger.info("No cached token found. Please visit the authorization URL.")
                auth_url = spotify_auth.get_authorize_url()
                logger.info(f"Visit this URL to authorize: {auth_url}")
                return False
            
            self.sp = spotipy.Spotify(auth=token_info['access_token'])
            logger.info("Spotify authentication successful")
            return True
        except Exception as e:
            logger.error(f"Spotify authentication failed: {e}")
            return False
    
    def search_song(self, artist, song, original_title):
        """Search for a song on Spotify"""
        if not self.sp:
            return None
        
        try:
            # Try different search queries
            search_queries = []
            
            if artist and song:
                search_queries.extend([
                    f'artist:"{artist}" track:"{song}"',
                    f'"{artist}" "{song}"',
                    f'{artist} {song}'
                ])
            
            # Add original title as fallback
            search_queries.append(f'"{original_title}"')
            search_queries.append(original_title)
            
            for query in search_queries:
                logger.info(f"Searching Spotify with query: {query}")
                results = self.sp.search(q=query, type='track', limit=5)
                
                if results['tracks']['items']:
                    track = results['tracks']['items'][0]
                    logger.info(f"Found track: {track['artists'][0]['name']} - {track['name']}")
                    return track
            
            logger.warning(f"No Spotify track found for: {original_title}")
            return None
            
        except Exception as e:
            logger.error(f"Error searching Spotify: {e}")
            return None
    
    def add_to_playlist(self, track_id):
        """Add a track to the specified playlist"""
        if not self.sp or not SPOTIFY_PLAYLIST_ID:
            return False
        
        try:
            self.sp.playlist_add_items(SPOTIFY_PLAYLIST_ID, [track_id])
            logger.info(f"Added track {track_id} to playlist")
            return True
        except Exception as e:
            logger.error(f"Error adding track to playlist: {e}")
            return False

class SlackBot:
    def __init__(self):
        self.youtube_extractor = YouTubeExtractor()
        self.spotify_manager = SpotifyManager()
        
    def extract_youtube_urls(self, text):
        """Extract YouTube URLs from text"""
        youtube_pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)'
        urls = re.findall(youtube_pattern, text)
        return [f"https://www.youtube.com/watch?v={video_id}" for video_id in urls]
    
    def process_youtube_url(self, url, channel_id, user_id):
        """Process a YouTube URL and add to Spotify playlist"""
        logger.info(f"Processing YouTube URL: {url}")
        
        # Extract song info from YouTube
        song_info = self.youtube_extractor.extract_song_info(url)
        if not song_info:
            self.send_message(channel_id, f"❌ Could not extract song info from: {url}")
            return
        
        # Search for the song on Spotify
        track = self.spotify_manager.search_song(
            song_info['artist'], 
            song_info['song'], 
            song_info['title']
        )
        
        if not track:
            message = f"❌ Could not find '{song_info['title']}' on Spotify"
            self.send_message(channel_id, message)
            return
        
        # Add to playlist
        success = self.spotify_manager.add_to_playlist(track['id'])
        
        if success:
            artist_names = ', '.join([artist['name'] for artist in track['artists']])
            message = f"✅ Added to playlist: **{artist_names} - {track['name']}**"
        else:
            message = f"❌ Failed to add '{track['name']}' to playlist"
        
        self.send_message(channel_id, message)
    
    def send_message(self, channel, text):
        """Send a message to Slack"""
        try:
            slack_client.chat_postMessage(channel=channel, text=text)
        except SlackApiError as e:
            logger.error(f"Error sending message: {e}")
    
    def handle_message(self, event):
        """Handle incoming Slack messages"""
        if event.get('subtype') == 'bot_message':
            return  # Ignore bot messages
        
        text = event.get('text', '')
        channel = event.get('channel')
        user = event.get('user')
        
        # Extract YouTube URLs
        youtube_urls = self.extract_youtube_urls(text)
        
        if youtube_urls:
            logger.info(f"Found {len(youtube_urls)} YouTube URLs in message")
            
            # Process each URL in a separate thread to avoid blocking
            for url in youtube_urls:
                thread = threading.Thread(
                    target=self.process_youtube_url,
                    args=(url, channel, user)
                )
                thread.start()

# Initialize bot
bot = SlackBot()

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    data = request.json
    
    # Handle URL verification challenge
    if data.get('type') == 'url_verification':
        return jsonify({'challenge': data.get('challenge')})
    
    # Handle events
    if data.get('type') == 'event_callback':
        event = data.get('event', {})
        
        if event.get('type') == 'message':
            bot.handle_message(event)
    
    return jsonify({'status': 'ok'})

@app.route('/callback')
def spotify_callback():
    """Handle Spotify OAuth callback"""
    code = request.args.get('code')
    if code:
        try:
            token_info = spotify_auth.get_access_token(code)
            return "Spotify authentication successful! You can close this window."
        except Exception as e:
            return f"Authentication failed: {e}"
    return "Authentication failed: No code received"

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True) 