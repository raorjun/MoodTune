import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import re
import os
from dotenv import load_dotenv

class PlaylistConverter:
    """
    A class with methods for converting playlists between Spotify and YouTube Music.
    """

    def __init__(self):
        """
        Initializes the PlaylistConverter by loading environment variables and setting up API clients for Spotify and YouTube Music.
        """
        dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
        load_dotenv(dotenv_path)
        self._spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri="https://localhost:5173/callback",
            scope="playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public",
        ))
        self._spotify_username = os.getenv("SPOTIFY_USERNAME")
        self._ytmusic = YTMusic("backend/config/browser.json")

    def get_spotify_tracks(self, playlist_url):
        """
        Extracts track names and artists from a Spotify playlist and stores them in a list.

        Args:
            playlist_url: The URL of the Spotify playlist.

        Returns:
            A list containing track names and artists.
        """
        playlist_id = re.search(r"playlist/([\w\d]+)", playlist_url).group(1)
        results = self._spotify.playlist_tracks(playlist_id)
        tracks = []  # Use a list instead of LinkedList

        for item in results['items']:
            track = item['track']
            track_str = f"{track['name']} {track['artists'][0]['name']}"
            tracks.append(track_str)  # Append each track to the list

        return tracks
        
    def get_youtube_tracks(self, playlist_url):
        """
        Extracts track names and artists from a YouTube Music playlist and stores them in a list.

        Args:
            playlist_url: The URL of the YouTube Music playlist.

        Returns:
            A list containing track names and artists.
        """
        playlist_id = re.search(r"list=([\w\d_-]+)", playlist_url).group(1)
        playlist = self._ytmusic.get_playlist(playlist_id)
        tracks = []  # Use a list instead of LinkedList

        for track in playlist["tracks"]:
            track_str = f"{track['title']} {track['artists'][0]['name']}"
            tracks.append(track_str)  # Append each track to the list

        return tracks

    def create_youtube_playlist(self, playlist_name, tracks):
        """
        Searches YouTube Music for tracks and creates a playlist with the given tracks.

        Args:
            playlist_name: The name of the new YouTube playlist.
            tracks: A list containing the track names and artists.

        Returns:
            A string URL of the newly created YouTube Music playlist, or None if the playlist creation fails.
        """
        video_ids = []

        while tracks:
            track = tracks.pop(0)  # Pop the first track from the list
            try:
                search_results = self._ytmusic.search(query=track, filter="songs", limit=1)
                if search_results:
                    video_id = search_results[0]["videoId"]
                    video_ids.append(video_id)
                else:
                    print(f"No results found for {track}")
            except Exception as e:
                print(f"Error searching for {track}: {e}")

        if video_ids:
            playlist_id = self._ytmusic.create_playlist(
                title=playlist_name,
                description="Converted from Spotify",
                video_ids=video_ids,
                privacy_status="PUBLIC"
            )
            return f"https://music.youtube.com/playlist?list={playlist_id}"

        return None

    def create_spotify_playlist(self, playlist_name, tracks):
        """
        Searches Spotify for tracks and creates a playlist with the given tracks.

        Args:
            playlist_name: The name of the new Spotify playlist.
            tracks: A list containing the track names and artists.

        Returns:
            A string URL of the newly created Spotify playlist.
        """
        playlist = self._spotify.user_playlist_create(
            user=self._spotify_username,
            name=playlist_name,
            public=True
        )

        spotify_uris = []

        while tracks:
            track = tracks.pop(0)  # Pop the first track from the list
            result = self._spotify.search(q=track, type="track", limit=1)
            if result["tracks"]["items"]:
                spotify_uris.append(result["tracks"]["items"][0]["uri"])
            else:
                print(f"No results found for {track}")

        self._spotify.user_playlist_add_tracks(
            user=self._spotify_username,
            playlist_id=playlist["id"],
            tracks=spotify_uris
        )

        return playlist["external_urls"]["spotify"]

    def convert_playlist(self, source_url, target_platform):
        """
        Converts a playlist between Spotify and YouTube Music.

        Args:
            source_url: The URL of the source playlist (either from Spotify or YouTube Music).
            target_platform: The platform to convert the playlist to ("spotify" or "youtube").

        Returns:
            A string URL of the converted playlist or an error message if the conversion fails.
        """
        if "spotify.com" in source_url:
            tracks = self.get_spotify_tracks(source_url)
            if target_platform == "youtube":
                return self.create_youtube_playlist("Converted Playlist", tracks)
        elif "youtube.com" in source_url:
            tracks = self.get_youtube_tracks(source_url)
            if target_platform == "spotify":
                return self.create_spotify_playlist("Converted Playlist", tracks)

        return "Invalid input or unsupported platform."


# Function to validate and handle user input
def get_valid_url(prompt, valid_platforms):
    """
    Simple URL checker for Spotify or YouTube playlists.
    """
    while True:
        url = input(prompt).strip()
        if any(platform in url for platform in valid_platforms):  # Check if URL matches valid platforms
            return url
        else:
            print("Invalid URL. Please enter a valid Spotify or YouTube playlist URL.")


def get_valid_platform(prompt, valid_platforms):
    """
    Prompts the user for a valid platform (either 'spotify' or 'youtube') and returns it.
    """
    while True:
        platform = input(prompt).strip().lower()
        if platform in valid_platforms:
            return platform
        else:
            print(f"Invalid platform. Please enter one of the following: {', '.join(valid_platforms)}.")


if __name__ == "__main__":
    # Define valid platforms
    valid_platforms = ["spotify", "youtube"]

    # Get user input with validation
    source_url = get_valid_url("Enter the playlist URL (Spotify or YouTube): ", valid_platforms)
    target_platform = get_valid_platform("Enter the target platform (spotify/youtube): ", valid_platforms)

    # Create a PlaylistConverter instance
    converter = PlaylistConverter()

    # Try to convert the playlist
    try:
        result = converter.convert_playlist(source_url, target_platform)
        print(f"Converted playlist: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
