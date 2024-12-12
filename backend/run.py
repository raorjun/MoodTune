from flask import Flask, request, redirect, url_for, session, jsonify
from converter import PlaylistConverter
from generator import PlaylistGenerator
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random key for session

# Initialize Playlist Generator
playlist_generator = PlaylistGenerator()

# Initialize Converter
playlist_converter = PlaylistConverter()


@app.route('/')
def home():
    return "Welcome to MoodTune!"

@app.route('/convert', methods=['POST'])
def convert():
    # Get form data from frontend
    source_url = request.form.get('source_url')
    target_platform = request.form.get('target_platform')

    if not source_url or not target_platform:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Calls the conversion method
        result_url = playlist_converter.convert_playlist(source_url, target_platform)

        if result_url:
            return jsonify({'url': result_url}), 200
        else:
            return jsonify({'error': 'Conversion failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_playlist():
    # Gets form data from the frontend
    seed_playlist_id = request.form.get('seed_playlist_id')
    seed_platform = request.form.get('seed_platform')
    target_energy = float(request.form.get('target_energy'))
    target_valence = float(request.form.get('target_valence'))
    activity = request.form.get('activity')
    environment = request.form.get('environment')
    amount = int(request.form.get('amount', 20))
    playlist_name = request.form.get('playlist_name', "Generated Playlist")

    # Validates required fields
    if not all([seed_playlist_id, seed_platform, target_energy, target_valence, amount]):
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        # Generates the playlist
        playlist_url = playlist_generator.generate_playlist_from_seed(
            seed_playlist_id=seed_playlist_id,
            seed_platform=seed_platform,
            target_energy=target_energy,
            target_valence=target_valence,
            activity=activity,
            environment=environment,
            amount=amount,
            playlist_name=playlist_name
        )
        return jsonify({'url': playlist_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)