import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
from data_structures import PriorityQueue
from dotenv import load_dotenv

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
    scope="playlist-modify-private"
))

# Do not forget to convert spotify playlist to yt music if user selects spotify as their app
# Function to generate a playlist based on user preferences
def generate_playlist(username, genre, energy, valence, activity, explicit, amount, environment, playlist_name="Generated Playlist"):
    
    if explicit == False:
        amount += 400
    else:
        amount += 100

    recommendations = None
    if environment == None: 
        recommendations = spotify.recommendations(
            seed_genres=genre.split(","),
            limit=amount,
            min_energy=energy - 0.2 if energy - 0.2 >= 0 else 0,
            max_energy=energy + 0.2 if energy + 0.2 <= 1 else 1,
            min_valence=valence - 0.2 if valence - 0.2 >= 0 else 0,
            max_valence=valence + 0.2 if valence + 0.2 <= 1 else 1
        )
    else:
        environments = {
            "gym": 0.8,
            "party": 0.9,
            "library": 0.2,
            "car": 0.6,
            "work": 0.4
        }
        aggressiveness = environments[environment]
        recommendations = spotify.recommendations(
            seed_genres=genre.split(", "),
            limit=amount,
            min_energy=energy - 0.2 if energy - 0.2 >= 0 else 0.0,
            max_energy=energy + 0.2 if energy + 0.2 <= 1 else 1.0,
            min_valence=valence - 0.2 if valence - 0.2 >= 0 else 0.0,
            max_valence=valence + 0.2 if valence + 0.2 <= 1 else 1.0,
            min_loudness=aggressiveness - 0.2 if aggressiveness - 0.2 >= 0 else 0.0,
            max_loudness=aggressiveness + 0.2 if aggressiveness + 0.2 <= 1 else 1.0
        )
    if not recommendations or not recommendations.get("tracks"):
        raise ValueError("No tracks found based on the provided parameters.")

    if activity != None:
        activities = {
            "running": 0.8,
            "studying": 0.3,
            "dancing": 0.9,
            "relaxing": 0.2
        }
        energy = activities[activity]
        recommendations = spotify.recommendations(
            seed_genres=genre.split(","),
            limit=100,
            target_energy=energy,
            target_valence=valence
        )
    tracks = generate_playlist_helper(recommendations, activity, amount)
    track_uris = [track["uri"] for track in tracks]

    # Creates a new Spotify playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False)
    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=track_uris)

    return playlist["external_urls"]["spotify"]

def generate_playlist_helper(recommendations, activity, amount):
    
    prioritized_tracks = PriorityQueue()
    for track in recommendations["tracks"]:
        track_features = spotify.audio_features(track["uri"])[0]
        weight = 0

        if activity == "working out":
            weight = track_features["loudness"] + track_features["energy"] + track_features["valence"]
        elif activity == "partying":
            weight = track_features["danceability"] + track_features["energy"] + track_features["loudness"]
        elif activity == "dancing":
            weight = track_features["danceability"]
        elif activity == "running":
            weight = track_features["energy"] + track_features["valence"]
        elif activity == "studying" or activity == "relaxing":
            weight = -track_features["valence"] - track_features["energy"] - track_features["loudness"]

        prioritized_tracks.insert(track, weight)

    top_tracks = [prioritized_tracks.pop() for _ in range(min(amount, prioritized_tracks.size()))]

    return top_tracks
        

# Main function to collect user input and generate a playlist
if __name__ == "__main__":

    print("Spotify Playlist Generator!")
    username = input("Enter your Spotify username: ")
    genre = input("Enter preferred genres (comma-separated, e.g., pop, rock): ")
    energy = float(input("Enter energy level (0.0 to 1.0): "))
    valence = float(input("Enter valence level (0.0 to 1.0, happiness measure): "))
    explicit = input("Allow explicit songs? (yes/no): ").strip().lower() == "yes"
    amount = int(input("Enter the number of tracks you want (e.g., 20): "))
    environment = input("Choose the environment (gym, party, library, car, work) or leave blank: ").strip().lower() or None
    activity = input("Choose an activity (running, studying, dancing, relaxing) or leave blank: ").strip().lower() or None
    playlist_name = input("Enter a name for your playlist (or leave blank for 'Generated Playlist'): ").strip() or "Generated Playlist"

    print("\nGenerating your playlist...")

    try:
        playlist_url = generate_playlist(
            username=username,
            genre=genre,
            energy=energy,
            valence=valence,
            activity=activity,
            explicit=explicit,
            amount=amount,
            environment=environment,
            playlist_name=playlist_name
        )
        print(f"\nYour playlist has been created! Open it here: {playlist_url}")
    except Exception as e:
        print("\nAn error occurred while generating the playlist.")
        print(f"Error details: {e}")