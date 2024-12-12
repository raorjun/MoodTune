import { useState } from 'react'
import spotifyIcon from './assets/spotify.svg'
import ytMusicIcon from './assets/youtube.svg'
import arrowIcon from './assests/arrow.svg'
//smiley face to frowny face svgs for mood
//number input for number of songs 5-30


function App() {
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [moodParams, setMoodParams] = useState({
    valence: 0.5,
    energy: 0.5,
    environment: '',
    activity: '',
    genre: '',
    songCount: 20,
    explicit: false
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <main className="container mx-auto px-4 py-12">
        {/*hero - main page*/}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white/90 mb-8">MoodTune</h1>
          <h2 className="text-7xl font-bold text-white mb-6">
            Your Mood, <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-500 to-violet-600 animate-gradient">Your Music</span>
          </h2>
          <p className="text-2xl text-white/80 mb-16">Generate playlists that match your emotional state</p>
        </div>

        {/* Platform Selection */}
        {!selectedPlatform && (
          <div className="max-w-md mx-auto space-y-4">
            <button
              onClick={() => setSelectedPlatform('spotify')}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg 
                bg-gradient-to-r from-blue-500 to-indigo-600 text-white 
                transition-all duration-300 hover:shadow-xl hover:scale-105
                hover:from-blue-600 hover:to-indigo-700"
            >
              <img src={spotifyIcon} alt="Spotify" className="w-6 h-6" />
              Connect with Spotify
            </button>
            <button
              onClick={() => setSelectedPlatform('ytmusic')}
              className="w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg 
                bg-gradient-to-r from-blue-500 to-indigo-600 text-white 
                transition-all duration-300 hover:shadow-xl hover:scale-105
                hover:from-blue-600 hover:to-indigo-700"
            >
              <img src={ytMusicIcon} alt="YouTube Music" className="w-6 h-6" />
              Connect with YouTube Music
            </button>
          </div>
        )}



        {/* Centered Go Back button */}
        {selectedPlatform && (
          <div className="flex justify-center mb-8">
            <button
              onClick={() => setSelectedPlatform(null)}
              className="flex items-center gap-2 px-4 py-2 rounded-lg 
                bg-white/10 text-white/80 hover:bg-white/20
                transition-all duration-300 hover:shadow-lg"
            >
              <img src={arrowIcon} alt="Go Back" className="w-5 h-5" />
              Go Back
            </button>
          </div>
        )}


        {/* Mood Input Form */}
        {selectedPlatform && (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="card-modern">
              <form className="space-y-6">
                {/* Mood Sliders */}
                <div className="space-y-4">
                  <div>
                    <label className="text-white text-sm mb-1 block">Mood</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={moodParams.valence}
                      onChange={(e) => setMoodParams({ ...moodParams, valence: parseInt(e.target.value) })}
                      className="w-full accent-white/80"
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Energy Level</label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={moodParams.energy}
                      onChange={(e) => setMoodParams({ ...moodParams, energy: parseInt(e.target.value) })}
                      className="w-full accent-white/80"
                    />
                  </div>
                </div>

                {/*context input*/}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-white text-sm mb-1 block">Environment</label>
                    <select
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      placeholder="Where are you?"
                      value={moodParams.environment}
                      onChange={(e) => setMoodParams({ ...moodParams, environment: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Activity</label>
                    <input
                      type="text"
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      placeholder="What are you doing?"
                      value={moodParams.activity}
                      onChange={(e) => setMoodParams({ ...moodParams, activity: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Genre</label>
                    <input
                      type="text"
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      placeholder="Preferred genre"
                      value={moodParams.genre}
                      onChange={(e) => setMoodParams({ ...moodParams, genre: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-white text-sm mb-1 block">Number of Songs</label>
                    <input
                      type="number"
                      min="10"
                      max="50"
                      className="w-full bg-white/10 rounded-lg px-4 py-2 text-white"
                      value={moodParams.songCount}
                      onChange={(e) => setMoodParams({ ...moodParams, songCount: parseInt(e.target.value) })}
                    />
                  </div>
                </div>

                {/* Settings */}
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="explicit"
                    checked={moodParams.explicit}
                    onChange={(e) => setMoodParams({ ...moodParams, explicit: e.target.checked })}
                    className="mr-2"
                  />
                  <label htmlFor="explicit" className="text-white text-sm">Allow explicit content</label>
                </div>

                {/* Submit Button */}
                <button className="w-full flex items-center justify-center gap-2 px-6 py-2 rounded-lg 
                  transition-all duration-300 bg-gradient-to-r from-blue-500 to-indigo-600 text-white 
                  hover:shadow-lg hover:scale-105">
                  Generate Playlist
                </button>
              </form>
            </div>

            {/* Graph Visualization */}
            <div className="card-modern min-h-[400px] flex items-center justify-center">
              <p className="text-white/60 text-center">
                Song correlation graph will appear here
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;