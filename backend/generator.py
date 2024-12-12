import csv
from dotenv import load_dotenv
import os
from data_structures import PriorityQueue
from converter import PlaylistConverter 
import re


class PlaylistGenerator:
    """
    A class for generating playlists based on seed playlists, user-specified criteria, and audio features.
    """

    def __init__(self):
        """
        Initializes the PlaylistGenerator by loading environment variables, setting up API clients,
        and preparing the PlaylistConverter for playlist creation on Spotify and YouTube.
        """
        dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
        load_dotenv(dotenv_path)
        self._converter = PlaylistConverter()  # Initialize the PlaylistConverter
        self._spotify = self._converter._spotify
        self._spotify_username = os.getenv("SPOTIFY_USERNAME")

    def fetch_seed_tracks(self, playlist_url, seed_platform):
        """
        Fetches tracks from a seed playlist on either Spotify or YouTube.
        Converts YouTube playlist to Spotify if necessary.

        Args:
            playlist_url: The URL of the playlist.
            seed_platform: The platform of the seed playlist ("spotify" or "youtube").

        Returns:
            A list of track information from the seed playlist.

        Raises:
            ValueError: If no tracks are found in the seed playlist.
        """
        url = playlist_url
        if seed_platform == "youtube":
            # Convert the YouTube playlist to a Spotify playlist URL
            url = self._converter.convert_playlist(playlist_url, "spotify")
        
        seed_tracks = []
        results = self._spotify.playlist_tracks(url)

        # Collect all tracks in the playlist (handle pagination)
        while results:
            seed_tracks.extend(results["items"])
            results = self._spotify.next(results) if results["next"] else None
        
        # Filter out any empty tracks
        seed_tracks = [track["track"] for track in seed_tracks if track["track"]]
        if not seed_tracks:  
            raise ValueError("No tracks found in the seed playlist")
        return seed_tracks


    def load_audio_features(self, csv_file="backend/tracks_features.csv"):
        """
        Loads audio features (energy, valence, danceability, loudness) from a CSV file.

        Args:
            csv_file: The path to the CSV file containing audio features.

        Returns:
            A dictionary mapping track IDs to their audio features.
        """
        audio_features = {}

        # Link to Kaggle Dataset CSV: https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs?resource=download)
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                song_id = row["id"]
                audio_features[song_id] = {
                    "energy": float(row["energy"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "loudness": float(row["loudness"]),
                }
        return audio_features

    def generate_playlist_from_seed(self, seed_playlist_url, seed_platform, target_platform, target_energy, target_valence, activity, environment, amount, playlist_name="Generated Playlist"):
        """
        Generates a playlist from a seed playlist based on the provided criteria such as target energy, 
        valence, activity, environment, and desired track amount.

        Args:
            seed_playlist_url: The URL of the seed playlist (either Spotify or YouTube).
            seed_platform: The platform of the seed playlist ("spotify" or "youtube").
            target_platform: The target platform for the generated playlist ("spotify" or "youtube").
            target_energy: The target energy for the playlist tracks (0 to 1).
            target_valence: The target valence (mood) for the playlist tracks (0 to 1).
            activity: The activity type (e.g., "working out", "relaxing").
            environment: The environment type (e.g., "gym", "party").
            amount: The number of tracks to include in the generated playlist.
            playlist_name: The name of the generated playlist.

        Returns:
            A string URL of the generated playlist on the target platform.
        
        Raises:
            ValueError: If no tracks are found in the seed playlist or if the target platform is invalid.
        """
        # Fetch the seed tracks from the given playlist URL
        seed_tracks = self.fetch_seed_tracks(seed_playlist_url, seed_platform)
        if not seed_tracks:
            raise ValueError("No tracks found in the seed playlist.")
 
        audio_features = self.load_audio_features()

        # Set the target loudness based on the activity type
        target_loudness = -7
        if activity in ["working out", "partying"]:
            target_loudness = -4
        elif activity in ["relaxing", "studying"]:
            target_loudness = -14

        # Define target danceability based on environment
        environment_danceability_map = {
            "gym": 0.7,
            "car": 0.6,
            "home": 0.4,
            "party": 0.9,
            "default": 0.5
        }
        target_danceability = environment_danceability_map.get(environment, environment_danceability_map["default"])

        # Initialize a priority queue to rank tracks by how well they match the targets
        prioritized_tracks = PriorityQueue()

        # Calculate a score for each track based on its similarity to the target features
        for track in seed_tracks:
            track_id = track["id"]
            if track_id in audio_features:
                features = audio_features[track_id]
                # Calculate a score based on the difference from the target values
                score = abs(features["energy"] - target_energy) \
                        + abs(features["valence"] - target_valence) \
                        + abs(features["loudness"] - target_loudness) \
                        + abs(features["danceability"] - target_danceability)
                # Insert the track into the priority queue with the calculated score (lower score = higher priority)
                prioritized_tracks.insert(track_id, -score)

        # Get the top tracks from the priority queue
        top_tracks = []
        for _ in range(min(amount, prioritized_tracks.size())):
            top_tracks.append(prioritized_tracks.pop())

        # Create a new playlist on Spotify
        playlist = self._spotify.user_playlist_create(user=self._spotify_username, name=playlist_name, public=True)
        self._spotify.user_playlist_add_tracks(user=self._spotify_username, playlist_id=playlist["id"], tracks=top_tracks)

        # Convert the playlist to the target platform
        if target_platform == "spotify":
            playlist_url = playlist["external_urls"]["spotify"]
        elif target_platform == "youtube":
            playlist_url = self._converter.convert_playlist(playlist["external_urls"]["spotify"], "youtube")
        else:
            raise ValueError("Unsupported target platform")

        return playlist_url

def get_valid_url(prompt):
    """
    Simple URL checker for Spotify or YouTube playlists.
    """
    while True:
        url = input(prompt).strip()
        # Check if the URL contains "spotify" or "youtube" as a basic validation
        if "spotify" in url or "youtube" in url:
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


def get_valid_float(prompt, min_value, max_value):
    """
    Prompts the user for a valid float value within a specified range.
    """
    while True:
        try:
            value = float(input(prompt).strip())
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Value must be between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_valid_activity(prompt, valid_activities):
    """
    Prompts the user for a valid activity (from a predefined list).
    """
    while True:
        activity = input(prompt).strip().lower()
        if activity in valid_activities:
            return activity
        else:
            print(f"Invalid activity. Please choose from {', '.join(valid_activities)}.")


def get_valid_environment(prompt, valid_environments):
    """
    Prompts the user for a valid environment (from a predefined list).
    """
    while True:
        environment = input(prompt).strip().lower()
        if environment in valid_environments:
            return environment
        else:
            print(f"Invalid environment. Please choose from {', '.join(valid_environments)}.")


def get_valid_amount(prompt, min_value, max_value):
    """
    Prompts the user for a valid amount (an integer within a specified range).
    """
    while True:
        try:
            amount = int(input(prompt).strip())
            if min_value <= amount <= max_value:
                return amount
            else:
                print(f"Amount must be between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


if __name__ == "__main__":
    generator = PlaylistGenerator()

    # Define valid platforms, activities, and environments
    valid_platforms = ["spotify", "youtube"]
    valid_activities = ["working out", "partying", "relaxing", "studying"]
    valid_environments = ["gym", "car", "home", "party"]

    try:
        # Get user inputs with validation
        seed_playlist_url = get_valid_url("Enter the playlist URL (Spotify or YouTube): ")
        seed_platform = get_valid_platform("Enter the seed platform (spotify/youtube): ", valid_platforms)
        target_platform = get_valid_platform("Enter the target platform (spotify/youtube): ", valid_platforms)

        target_energy = get_valid_float("Enter the target energy (0 to 1): ", 0, 1)
        target_valence = get_valid_float("Enter the target valence (0 to 1): ", 0, 1)

        activity = get_valid_activity("Enter the activity type (working out, partying, relaxing, studying): ", valid_activities)
        environment = get_valid_environment("Enter the environment type (gym, car, home, party): ", valid_environments)

        amount = get_valid_amount("Enter the number of tracks to include in the playlist (1 to 30): ", 1, 30)

        # Generate playlist
        playlist_url = generator.generate_playlist_from_seed(
            seed_playlist_url=seed_playlist_url,
            seed_platform=seed_platform,
            target_platform=target_platform,
            target_energy=target_energy,
            target_valence=target_valence,
            activity=activity,
            environment=environment,
            amount=amount,
            playlist_name="Generated Playlist"
        )

        print(f"Generated playlist: {playlist_url}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred while generating the playlist: {e}")