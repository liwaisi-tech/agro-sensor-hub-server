export function Footer() {
  return (
    <footer className="bg-green-500 dark:bg-green-700 text-white p-4 mt-auto">
      <div className="container mx-auto">
        <p className="text-center">© {new Date().getFullYear()} Tecnología de Innovación en <a href="https://liwaisi.tech" className="underline hover:text-green-200 transition-colors" target="_blank" rel="noopener noreferrer">liwaisi.tech</a>.</p>
      </div>
    </footer>
  )
} 