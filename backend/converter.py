import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from ytmusicapi import YTMusic
import ytmusicapi
import re
import os
from dotenv import load_dotenv
import json

# Spotify API credentials
dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path)
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "https://localhost:5173/callback"

# Set up Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public"
))

"""
def get_ytmusic_with_new_token():
    oauth_path = "backend/config/oauth.json"

    # If old credentials exist, delete them
    if os.path.exists(oauth_path):
        os.remove(oauth_path)
    
    # Reinitialize YTMusic with a new token (interactive flow)
    ytmusicapi.setup(filepath=oauth_path)
    return YTMusic(oauth_path)
"""

# Load YouTube Music OAuth credentials
ytmusic = YTMusic("backend/config/browser.json")

# Function to extract Spotify playlist tracks
def get_spotify_tracks(playlist_url):
    playlist_id = re.search(r"playlist/([\w\d]+)", playlist_url).group(1)
    results = spotify.playlist_tracks(playlist_id)
    tracks = []

    for item in results['items']:
        track = item['track']
        tracks.append(f"{track['name']} {track['artists'][0]['name']}")

    return tracks

# Function to search YouTube Music and create a playlist
def create_youtube_playlist(playlist_name, tracks):
    video_ids = []
    for track in tracks:
        try:
            # Perform search for each track (song filter)
            search_results = ytmusic.search(query=track, filter="songs", limit=1)

            if search_results:
                # Assuming the first result is the correct one
                video_id = search_results[0]["videoId"]
                video_ids.append(video_id)
                print(f"Found video for {track}: {video_id}")
            else:
                print(f"No results found for {track}")
        except Exception as e:
            print(f"Error searching for {track}: {e}")
    
    # If we have valid video IDs, create the playlist
    if video_ids:
        playlist_id = ytmusic.create_playlist(title=playlist_name, description="Converted from Spotify", video_ids=video_ids, privacy_status="PUBLIC")
        return f"https://music.youtube.com/playlist?list={playlist_id}"
    else:
        print("No valid tracks found for playlist.")
        return None

# Function to extract YouTube Music playlist tracks
def get_youtube_tracks(playlist_url):
    playlist_id = re.search(r"list=([\w\d_-]+)", playlist_url).group(1)
    playlist = ytmusic.get_playlist(playlist_id)
    tracks = []

    for track in playlist["tracks"]:
        tracks.append(f"{track['title']} {track['artists'][0]['name']}")

    return tracks

# Function to search Spotify and create a playlist
def create_spotify_playlist(username, playlist_name, tracks):
    # Create a new Spotify playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False)

    spotify_uris = []
    for track in tracks:
        result = spotify.search(q=track, type="track", limit=1)
        if result["tracks"]["items"]:
            spotify_uris.append(result["tracks"]["items"][0]["uri"])
            print(f"Found track for {track}")
        else:
            print(f"No results found for {track}")

    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=spotify_uris, public=True)

    return playlist["external_urls"]["spotify"]

# Main function to handle conversion
def convert_playlist(source_url, target_platform, spotify_username):
    if "spotify.com" in source_url:
        # Convert Spotify to YouTube Music
        tracks = get_spotify_tracks(source_url)
        if target_platform == "youtube":
            return create_youtube_playlist("Converted Playlist", tracks)
    elif "youtube.com" in source_url:
        # Convert YouTube Music to Spotify
        tracks = get_youtube_tracks(source_url)
        if target_platform == "spotify":
            return create_spotify_playlist(spotify_username, "Converted Playlist", tracks)

    return "Invalid input or unsupported platform."

source_url = input("Enter the playlist URL: ")
target_platform = input("Enter target platform (spotify/youtube): ")
spotify_username = input("Enter your Spotify username: ") if target_platform == "spotify" else None

result = convert_playlist(source_url, target_platform, spotify_username)
print(f"Converted playlist: {result}")