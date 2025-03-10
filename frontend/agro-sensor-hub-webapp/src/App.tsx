import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { Dashboard } from './components/Dashboard'
import { NotFound } from './components/NotFound'
import { History } from './components/History'

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
    <Router>
      <div className="min-h-screen flex flex-col w-full m-0 p-0 bg-white dark:bg-gray-900 transition-colors duration-200">
        <Header isDarkMode={isDarkMode} onToggleDarkMode={toggleDarkMode} />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/history" element={<History />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  )
}

export default App
