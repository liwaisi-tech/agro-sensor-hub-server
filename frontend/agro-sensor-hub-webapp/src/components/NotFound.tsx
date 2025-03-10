import { useNavigate } from 'react-router-dom';
import { IoHomeOutline } from 'react-icons/io5';

export const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-white dark:bg-gray-900 p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4 text-gray-800 dark:text-white">
          La página que buscas no fue encontrada
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          Prueba modificando la url o dando click al ícono de inicio a continuación
        </p>
        <button
          onClick={() => navigate('/')}
          className="p-4 rounded-full bg-blue-500 hover:bg-blue-600 transition-colors duration-200 text-white"
          aria-label="Ir al inicio"
        >
          <IoHomeOutline className="w-8 h-8" />
        </button>
      </div>
    </div>
  );
}; 