import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import csv
from dotenv import load_dotenv
from data_structures import PriorityQueue

# Load Spotify API credentials
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

# Function to fetch tracks from a seed playlist
def fetch_seed_tracks(seed_playlist_id):
    seed_tracks = []
    results = spotify.playlist_tracks(seed_playlist_id)
    while results:
        seed_tracks.extend(results["items"])
        results = spotify.next(results) if results["next"] else None
    return [track["track"] for track in seed_tracks if track["track"]]

# Function to load audio features from a CSV file
def load_audio_features(csv_file="backend/tracks_features.csv"):
    audio_features = {}
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Read as a dictionary using the header row
        for row in reader:
            song_id = row["id"]
            audio_features[song_id] = {
                "energy": float(row["energy"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "loudness": float(row["loudness"]),
            }
    return audio_features

# Generate playlist using user-defined targets and minimal difference scoring
def generate_playlist_from_seed(username, seed_playlist_id, csv_file, target_energy, target_valence, activity, environment, amount, playlist_name="Generated Playlist"):
    seed_tracks = fetch_seed_tracks(seed_playlist_id)
    if not seed_tracks:
        raise ValueError("No tracks found in the seed playlist.")

    # Load audio features from the CSV file
    audio_features = load_audio_features(csv_file)

    # Define target loudness based on activity
    target_loudness = -7
    if activity in ["working out", "partying"]:
        target_loudness = -4
    elif activity in ["relaxing, studying"]:
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

    # Priority queue for ranking tracks
    prioritized_tracks = PriorityQueue()

    # Calculate score for each track based on minimal difference from targets
    for track in seed_tracks:
        track_id = track["id"]
        if track_id in audio_features:
            features = audio_features[track_id]
            score = abs(features["energy"] - target_energy) \
                    + abs(features["valence"] - target_valence) \
                    + abs(features["loudness"] - target_loudness) \
                    + abs(features["danceability"] - target_danceability)
            # Insert with score (lower score = higher priority)
            prioritized_tracks.insert(track_id, -score)

    # Get the top tracks based on the priority queue
    top_tracks = []
    for _ in range(min(amount, prioritized_tracks.size())):
        top_tracks.append(prioritized_tracks.pop())

    # Create a new playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=True)
    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=top_tracks)

    return playlist["external_urls"]["spotify"]

# Main function to collect user input and generate a playlist
if __name__ == "__main__":
    print("Spotify Playlist Generator!")
    username = input("Enter your Spotify username: ")
    seed_playlist_id = input("Enter the seed playlist ID: ")
    target_energy = float(input("Enter target energy level (0.0 to 1.0): "))
    target_valence = float(input("Enter target valence level (0.0 to 1.0): "))
    activity = input("Enter the activity (working out, partying, studying, relaxing): ").strip().lower()
    environment = input("Enter the environment (gym, car, home, party): ").strip().lower()
    amount = int(input("Enter the number of tracks you want: "))
    playlist_name = input("Enter a name for your playlist: ").strip() or "Generated Playlist"

    try:
        print("\nGenerating your playlist...")
        playlist_url = generate_playlist_from_seed(
            username=username,
            seed_playlist_id=seed_playlist_id,
            csv_file="backend/tracks_features.csv",
            target_energy=target_energy,
            target_valence=target_valence,
            activity=activity,
            environment=environment,
            amount=amount,
            playlist_name=playlist_name
        )
        print(f"Your playlist has been created! Open it here: {playlist_url}")
    except Exception as e:
        print(f"\nAn error occurred while generating the playlist: {e}")
