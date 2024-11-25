import { useState } from 'react'
import spotifyIcon from './assets/spotify.svg'

function App() {
  const [activeTab, setActiveTab] = useState('features');

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      {/* Navigation */}
      <header className="glass fixed w-full z-50">
        <nav className="max-w-6xl mx-auto p-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-white">MoodTune</h1>
            
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="pt-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-6xl font-bold text-white mb-6">
              Your Music, <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-400">Your Mood</span>
            </h2>
            <p className="text-xl text-white/80 mb-8">Generate playlists that match your mood</p>
            <button className="btn-modern flex items-center gap-2 mx-auto">
              <img src={spotifyIcon} alt="Spotify" className="w-6 h-6" />
              Connect with Spotify
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App