import React, { useEffect } from 'react';

interface ModalProps {
  children: React.ReactNode;
  onClose: () => void;
}

export function Modal({ children, onClose }: ModalProps) {
  useEffect(() => {
    // Disable scrolling on the body when modal is open
    document.body.style.overflow = 'hidden';

    // Re-enable scrolling when modal is closed
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white dark:bg-gray-800 rounded-lg w-full h-full max-w-7xl max-h-[90vh] overflow-auto relative">
        <button
          onClick={onClose}
          className="absolute top-0 right-0 p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        {children}
      </div>
    </div>
  );
} 