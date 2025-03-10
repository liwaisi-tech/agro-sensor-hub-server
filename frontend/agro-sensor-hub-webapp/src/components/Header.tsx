import { CgDarkMode, CgBell } from 'react-icons/cg'

interface HeaderProps {
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

export function Header({ isDarkMode, onToggleDarkMode }: HeaderProps) {
  return (
    <header className="bg-blue-500 dark:bg-blue-700 text-white w-full p-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold">Agro Sensor Hub</h1>
        <div className="flex items-center gap-4">
          <button 
            onClick={onToggleDarkMode}
            className="p-2 bg-blue-400 dark:bg-blue-600 hover:bg-blue-500 dark:hover:bg-blue-500 rounded-full transition-colors"
            title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            <CgDarkMode size={24} className={isDarkMode ? "text-yellow-300" : ""} />
          </button>
          <button className="p-2 bg-blue-400 dark:bg-blue-600 hover:bg-blue-500 dark:hover:bg-blue-500 rounded-full transition-colors">
            <CgBell size={24} />
          </button>
        </div>
      </div>
    </header>
  )
} 