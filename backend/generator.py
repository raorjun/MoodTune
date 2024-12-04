import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os
import dotenv

# Spotify API credentials
dotenv.load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "https://localhost:5173/callback"

# Setting up Spotify client for authentication
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-private"
))

# Do not forget to convert spotify playlist to yt music if user selects spotify as their app
# Function to generate a playlist based on user preferences
def generate_playlist(username, genre, energy, valence, activity, explicit, amount, environment, playlist_name="Generated Playlist"):
    # Using Spotify's recommendations endpoint

    if explicit == False:
        amount += 400
    else:
        amount += 100
        
    recommendations = None
    if environment == None:
        recommendations = spotify.recommendations(
            seed_genres=genre.split(","),
            limit=amount,
            target_energy=energy,
            target_valence=valence
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
            seed_genres=genre.split(","),
            limit=100,
            target_energy=energy,
            target_valence=valence,
            target_loudness=aggressiveness
        )


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
    track_uris = [track["uri"] for track in recommendations["tracks"]]

    # Creates a new Spotify playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False)
    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=track_uris)

    return playlist["external_urls"]["spotify"]

def generate_playlist_helper(recommendations, activity, amount):
    for playlist in playlists:
        if playlist["name"] == "Generated Playlist":
            return playlist["external_urls"]["spotify"]
    
    return generate_playlist(username, genre, energy, valence, aggressiveness)

# Main function to collect user input and generate a playlist
if __name__ == "__main__":
    print("Welcome to the Spotify Playlist Generator!")
    username = input("Enter your Spotify username: ")
    genre = input("Enter preferred genres (comma-separated, e.g., pop, rock): ")
    energy = float(input("Enter energy level (0.0 to 1.0): "))
    valence = float(input("Enter valence level (0.0 to 1.0, happiness measure): "))
    aggressiveness = float(input("Enter aggressiveness (target loudness in dB, e.g., -10 for aggressive, -30 for calm): "))

    print("Generating your playlist...")
    playlist_url = generate_playlist(username, genre, energy, valence, aggressiveness)

    print(f"Your playlist has been created! Open it here: {playlist_url}")