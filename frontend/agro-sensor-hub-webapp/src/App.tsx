import { useState, useEffect } from 'react'
import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { Dashboard } from './components/Dashboard'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const savedMode = localStorage.getItem('darkMode')
    return savedMode ? JSON.parse(savedMode) : false
  })

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(isDarkMode))
    if (isDarkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [isDarkMode])

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
  }

  return (
    <div className="min-h-screen flex flex-col w-full m-0 p-0 bg-white dark:bg-gray-900 transition-colors duration-200">
      <Header isDarkMode={isDarkMode} onToggleDarkMode={toggleDarkMode} />
      <Dashboard />
      <Footer />
    </div>
  )
}

export default App
