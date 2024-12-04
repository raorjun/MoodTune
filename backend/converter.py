import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
import re
import os
import dotenv

# Spotify API credentials
dotenv.load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "https://localhost:5173/callback"

# Set up Spotify client
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-private"
))

# Set up YouTube Music client
ytmusic = YTMusic("oauth.json")  # Need to generate and provide this file

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
    # Search for each track on YouTube Music and collect video IDs
    video_ids = []
    for track in tracks:
        search_results = ytmusic.search(query=track, filter="songs")
        if search_results:
            video_ids.append(search_results[0]["videoId"])

    # Create a new YouTube Music playlist
    playlist_id = ytmusic.create_playlist(
        title=playlist_name, description="Converted from Spotify", video_ids=video_ids
    )

    return f"https://music.youtube.com/playlist?list={playlist_id}"

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

    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=spotify_uris)

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

if __name__ == "__main__":
    source_url = input("Enter the playlist URL: ")
    target_platform = input("Enter target platform (spotify/youtube): ")
    spotify_username = input("Enter your Spotify username: ") if target_platform == "spotify" else None

    result = convert_playlist(source_url, target_platform, spotify_username)
    print(f"Converted playlist: {result}")