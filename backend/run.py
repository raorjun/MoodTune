from flask import Flask, request, jsonify
from flask_cors import CORS
from converter import PlaylistConverter
from generator import PlaylistGenerator
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Optional: only needed if using sessions
CORS(app)  # Enable CORS for all routes

# Initialize Playlist Generator and Converter
playlist_generator = PlaylistGenerator()
playlist_converter = PlaylistConverter()

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the MoodTune API'}), 200

@app.route('/convert', methods=['POST'])
def convert_playlist():
    data = request.get_json()

    # Validate required fields
    if not all(key in data for key in ['playlist_url', 'target_platform']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        converted_url = playlist_converter.convert_playlist(
            source_url=data['playlist_url'],
            target_platform=data['target_platform']
        )
        print(converted_url)
        return jsonify({'url': converted_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/generate', methods=['POST'])
def generate_playlist():
    data = request.get_json()

    # Validate required fields
    required_fields = [
        'seed_playlist_id', 'seed_platform', 'target_platform', 'target_energy',
        'target_valence', 'activity', 'environment', 'amount', 'playlist_name'
    ]
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        playlist_url = playlist_generator.generate_playlist_from_seed(
            seed_playlist_id=data['seed_playlist_id'],
            seed_platform=data['seed_platform'],
            target_platform=data['target_platform'],
            target_energy=data['target_energy'],
            target_valence=data['target_valence'],
            activity=data['activity'],
            environment=data['environment'],
            amount=data['amount'],
            playlist_name=data['playlist_name']
        )
        return jsonify({'url': playlist_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
