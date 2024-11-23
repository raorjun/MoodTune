import { useState } from 'react'

function App() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-blue-600 p-4">
        <nav className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-white font-bold text-xl">My Website</h1>
          
          {/* Mobile menu button */}
          <button 
            className="md:hidden text-white"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            Menu
          </button>

          {/* Desktop menu */}
          <ul className="hidden md:flex space-x-4">
            <li><a href="#" className="text-white hover:text-blue-200">Home</a></li>
            <li><a href="#" className="text-white hover:text-blue-200">About</a></li>
            <li><a href="#" className="text-white hover:text-blue-200">Contact</a></li>
          </ul>

          {/* Mobile menu */}
          {isMobileMenuOpen && (
            <ul className="absolute top-16 left-0 right-0 bg-blue-600 p-4 md:hidden">
              <li><a href="#" className="block py-2 text-white hover:text-blue-200">Home</a></li>
              <li><a href="#" className="block py-2 text-white hover:text-blue-200">About</a></li>
              <li><a href="#" className="block py-2 text-white hover:text-blue-200">Contact</a></li>
            </ul>
          )}
        </nav>
      </header>
    </div>
  )
}

export default App