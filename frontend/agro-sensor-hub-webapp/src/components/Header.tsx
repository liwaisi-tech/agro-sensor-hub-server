import { CgDarkMode, CgBell } from 'react-icons/cg'
import { Link, useLocation } from 'react-router-dom'

interface HeaderProps {
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

export function Header({ isDarkMode, onToggleDarkMode }: HeaderProps) {
  const location = useLocation();
  
  return (
    <header className="bg-blue-500 dark:bg-blue-700 text-white w-full p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center gap-8">
          <nav className="flex gap-4">
            <Link 
              to="/" 
              className={`hover:text-blue-200 transition-colors ${location.pathname === '/' ? 'text-blue-200' : ''}`}
            >
              Dashboard
            </Link>
            <Link 
              to="/history" 
              className={`hover:text-blue-200 transition-colors ${location.pathname === '/history' ? 'text-blue-200' : ''}`}
            >
              Historial
            </Link>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={onToggleDarkMode}
            className="p-2 bg-blue-400 dark:bg-blue-600 hover:bg-blue-500 dark:hover:bg-blue-500 rounded-full transition-colors"
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            <CgDarkMode size={24} className={isDarkMode ? "text-white" : "text-black"} />
          </button>
          <button className="p-2 bg-blue-400 dark:bg-blue-600 hover:bg-blue-500 dark:hover:bg-blue-500 rounded-full transition-colors">
            <CgBell size={24} />
          </button>
        </div>
      </div>
    </header>
  )
} 