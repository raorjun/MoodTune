import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Setting up Spotify client for authentication
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-private"
))

# Function to generate a playlist based on user preferences
def generate_playlist(username, genre, energy, valence, aggressiveness, playlist_name="Generated Playlist"):
    # Using Spotify's recommendations endpoint
    recommendations = spotify.recommendations(
        seed_genres=genre.split(","),
        limit=100,
        target_energy=energy,
        target_valence=valence,
        target_loudness=aggressiveness
    )

    track_uris = [track["uri"] for track in recommendations["tracks"]]

    # Creates a new Spotify playlist
    playlist = spotify.user_playlist_create(user=username, name=playlist_name, public=False)
    spotify.user_playlist_add_tracks(user=username, playlist_id=playlist["id"], tracks=track_uris)

    return playlist["external_urls"]["spotify"]

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