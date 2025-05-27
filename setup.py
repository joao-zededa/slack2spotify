#!/usr/bin/env python3
"""
Setup script for Slack2Spotify bot.
This script helps with initial Spotify authentication.
"""

import os
import webbrowser
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    print("🎵 Slack2Spotify Bot Setup")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file based on config.env.example")
        return
    
    # Get Spotify credentials
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    
    if not all([client_id, client_secret, redirect_uri]):
        print("❌ Spotify credentials missing in .env file!")
        print("Please set SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REDIRECT_URI")
        return
    
    # Initialize Spotify OAuth
    scope = 'playlist-modify-public playlist-modify-private'
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    
    print("🔐 Starting Spotify authentication...")
    
    # Check for cached token
    token_info = sp_oauth.get_cached_token()
    
    if token_info:
        print("✅ Found cached Spotify token!")
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        try:
            user = sp.current_user()
            print(f"✅ Authenticated as: {user['display_name']} ({user['id']})")
            
            # List user's playlists
            playlists = sp.current_user_playlists(limit=10)
            print("\n📋 Your playlists:")
            for i, playlist in enumerate(playlists['items'], 1):
                print(f"  {i}. {playlist['name']} (ID: {playlist['id']})")
            
            print(f"\n💡 To use a playlist, add this to your .env file:")
            print(f"SPOTIFY_PLAYLIST_ID=<playlist_id>")
            
        except Exception as e:
            print(f"❌ Error testing Spotify connection: {e}")
    else:
        print("🌐 Opening browser for Spotify authentication...")
        auth_url = sp_oauth.get_authorize_url()
        print(f"Visit this URL: {auth_url}")
        
        try:
            webbrowser.open(auth_url)
        except:
            print("Could not open browser automatically.")
        
        print("\nAfter authorizing, you'll be redirected to your redirect URI.")
        print("Run this script again after authorization to verify the setup.")

if __name__ == '__main__':
    main() 