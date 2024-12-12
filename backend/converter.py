import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import re
import os
from dotenv import load_dotenv


class PlaylistConverter:
    def __init__(self):
        # Load Spotify API credentials
        dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
        load_dotenv(dotenv_path)
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri="https://localhost:5173/callback",
            scope="playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public",
        ))
        self.spotify_username = os.getenv("SPOTIFY_USERNAME")
        self.ytmusic = YTMusic("backend/config/browser.json")

    def get_spotify_tracks(self, playlist_url):
        """
        Extracts track names and artists from a Spotify playlist.
        """
        playlist_id = re.search(r"playlist/([\w\d]+)", playlist_url).group(1)
        results = self.spotify.playlist_tracks(playlist_id)
        tracks = []

        for item in results['items']:
            track = item['track']
            tracks.append(f"{track['name']} {track['artists'][0]['name']}")

        return tracks
        
    def get_youtube_tracks(self, playlist_url):
        """
        Extracts track names and artists from a YouTube Music playlist.
        """
        playlist_id = re.search(r"list=([\w\d_-]+)", playlist_url).group(1)
        playlist = self.ytmusic.get_playlist(playlist_id)
        tracks = []

        for track in playlist["tracks"]:
            tracks.append(f"{track['title']} {track['artists'][0]['name']}")

        return tracks

    def create_youtube_playlist(self, playlist_name, tracks):
        """
        Searches YouTube Music and creates a playlist with the given tracks.
        """
        video_ids = []
        for track in tracks:
            try:
                search_results = self.ytmusic.search(query=track, filter="songs", limit=1)
                if search_results:
                    video_id = search_results[0]["videoId"]
                    video_ids.append(video_id)
                else:
                    print(f"No results found for {track}")
            except Exception as e:
                print(f"Error searching for {track}: {e}")

        if video_ids:
            playlist_id = self.ytmusic.create_playlist(
                title=playlist_name,
                description="Converted from Spotify",
                video_ids=video_ids,
                privacy_status="PUBLIC"
            )
            return f"https://music.youtube.com/playlist?list={playlist_id}"

        return None

    def create_spotify_playlist(self, playlist_name, tracks):
        """
        Searches Spotify and creates a playlist with the given tracks.
        """
        playlist = self.spotify.user_playlist_create(
            user=self.spotify_username,
            name=playlist_name,
            public=True
        )

        spotify_uris = []
        for track in tracks:
            result = self.spotify.search(q=track, type="track", limit=1)
            if result["tracks"]["items"]:
                spotify_uris.append(result["tracks"]["items"][0]["uri"])
            else:
                print(f"No results found for {track}")

        self.spotify.user_playlist_add_tracks(
            user=self.spotify_username,
            playlist_id=playlist["id"],
            tracks=spotify_uris
        )

        return playlist["external_urls"]["spotify"]

    def convert_playlist(self, source_url, target_platform):
        """
        Converts a playlist between Spotify and YouTube Music.
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


# Testing the Converter
if __name__ == "__main__":
    source_url = input("Enter the playlist URL: ")
    target_platform = input("Enter target platform (spotify/youtube): ")

    converter = PlaylistConverter()
    result = converter.convert_playlist(source_url, target_platform)
    print(f"Converted playlist: {result}")