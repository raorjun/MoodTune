import { useState } from 'react';
import spotifyIcon from './assets/spotify.svg';
import ytMusicIcon from './assets/youtube.svg';
import arrowIcon from './assets/arrow.svg';

function App() {
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [showPlatformSelect, setShowPlatformSelect] = useState(false);
  const [isConverting, setIsConverting] = useState(false);
  const [playlistUrl, setPlaylistUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [moodParams, setMoodParams] = useState({
    seed_playlist_id: '',
    seed_platform: '',
    target_platform: '',
    target_energy: 0.5,
    target_valence: 0.5,
    activity: '',
    environment: '',
    songCount: 20,
    playlist_name: '',
  });

  const handleGenerate = () => {
    setIsConverting(false);
    setShowPlatformSelect(true);
  };

  const handleConvertClick = () => {
    setIsConverting(true);
    setShowPlatformSelect(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          seed_playlist_id: moodParams.seed_playlist_id,
          seed_platform: moodParams.seed_platform,
          target_platform: moodParams.target_platform,
          target_energy: moodParams.target_energy,
          target_valence: moodParams.target_valence,
          activity: moodParams.activity,
          environment: moodParams.environment,
          amount: moodParams.songCount,
          playlist_name: moodParams.playlist_name,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate playlist');
      }

      const data = await response.json();
      window.open(data.url, '_blank');
    } catch (err) {
      setError('Failed to generate playlist. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleConvert = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          playlist_url: playlistUrl,
          target_platform: selectedPlatform,
        }),
      });
  
      const data = await response.json();
      console.log(data);  // Log the response data
  
      if (response.ok) {
        if (data.url) {
          console.log('Opening URL:', data.url);  // Log URL to verify it's correct
          window.open(data.url, '_blank');  // Open the playlist URL in a new tab
        } else {
          throw new Error('No URL returned from the server');
        }
      } else {
        throw new Error(data.error || 'Failed to convert playlist');
      }
    } catch (err) {
      console.error('Error:', err.message);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <main className="container mx-auto px-4 py-12">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white/90 mb-8">MoodTune</h1>
          <h2 className="text-7xl font-bold text-white mb-6">
            Your Mood,{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-500 to-violet-600 animate-gradient">
              Your Music
            </span>
          </h2>
          <p className="text-2xl text-white/80 mb-16">Generate playlists that match your emotional state</p>
        </div>

        {/* Home Page Buttons */}
        {!showPlatformSelect && !selectedPlatform && (
          <div className="max-w-md mx-auto space-y-4">
            <button
              onClick={handleGenerate}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 text-white"
            >
              Generate New Playlist
            </button>
            <button
              onClick={handleConvertClick}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-violet-600 text-white"
            >
              Convert Existing Playlist
            </button>
          </div>
        )}

        {/* Platform Selection */}
        {showPlatformSelect && !selectedPlatform && (
          <div className="max-w-md mx-auto space-y-4">
            <p className="text-white text-center mb-4">
              {isConverting ? 'Select platform to convert to:' : 'Choose your platform:'}
            </p>
            <button
              onClick={() => setSelectedPlatform('spotify')}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 text-white"
            >
              <img src={spotifyIcon} alt="Spotify" className="w-6 h-6" />
              Connect with Spotify
            </button>
            <button
              onClick={() => setSelectedPlatform('ytmusic')}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg bg-gradient-to-r from-blue-500 to-indigo-600 text-white"
            >
              <img src={ytMusicIcon} alt="YouTube Music" className="w-6 h-6" />
              Connect with YouTube Music
            </button>
          </div>
        )}

        {/* Go Back Button */}
        {(showPlatformSelect || selectedPlatform) && (
          <div className="flex justify-center mt-8 mb-4">
            <button
              onClick={() => {
                setSelectedPlatform(null);
                setShowPlatformSelect(false);
                setIsConverting(false);
                setPlaylistUrl('');
                setError(null);
              }}
              className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white/10 text-white/80"
            >
              <img src={arrowIcon} alt="Go Back" className="w-5 h-5" />
              Go Back
            </button>
          </div>
        )}

        {/* Conversion Form */}
        {isConverting && selectedPlatform && (
          <div className="max-w-md mx-auto">
            <form onSubmit={handleConvert} className="space-y-6">
              <div>
                <label className="text-white text-sm mb-2 block">Paste your playlist link:</label>
                <input
                  type="url"
                  value={playlistUrl}
                  onChange={(e) => setPlaylistUrl(e.target.value)}
                  placeholder="https://open.spotify.com/playlist/..."
                  required
                  className="w-full bg-white/10 rounded-lg px-4 py-2 text-white border border-white/20"
                />
              </div>

              {error && <div className="text-red-400 text-sm text-center">{error}</div>}

              <button
                type="submit"
                disabled={isLoading}
                className="w-full flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-violet-600 text-white"
              >
                {isLoading ? 'Converting...' : 'Convert Playlist'}
              </button>
            </form>
          </div>
        )}

        {/* Mood Input Form */}
        {selectedPlatform && !isConverting && (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="card-modern">
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Mood Sliders */}
                <div className="space-y-4">
                  <div>
                    <label className="text-white text-sm mb-1 block">Mood</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={moodParams.target_valence * 100}
                      onChange={(e) => setMoodParams({ ...moodParams, target_valence: parseInt(e.target.value) / 100 })}
                      className="w-full accent-white/80"
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Energy Level</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={moodParams.target_energy * 100}
                      onChange={(e) => setMoodParams({ ...moodParams, target_energy: parseInt(e.target.value) / 100 })}
                      className="w-full accent-white/80"
                    />
                  </div>
                </div>

                {/* Context Input */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-white text-sm mb-1 block">Environment</label>
                    <input
                      type="text"
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      value={moodParams.environment}
                      onChange={(e) => setMoodParams({ ...moodParams, environment: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Activity</label>
                    <input
                      type="text"
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      value={moodParams.activity}
                      onChange={(e) => setMoodParams({ ...moodParams, activity: e.target.value })}
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full px-6 py-3 rounded-lg bg-gradient-to-r from-purple-500 to-violet-600 text-white"
                  >
                    {isLoading ? 'Generating...' : 'Generate Playlist'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
