import { PlantingBox } from './PlantingBox';
import { CgDetailsMore } from 'react-icons/cg';

interface ZoneProps {
  id: string;
  boxes: {
    envTemp: number;
    groundHumidity: number;
    envHumidity: number;
    status: 'active' | 'inactive';
  }[];
  onZoneClick: () => void;
}

export function Zone({ id, boxes, onZoneClick }: ZoneProps) {
  return (
    <div 
      className="bg-white dark:bg-gray-700 rounded-lg shadow p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-600"
    >
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-800 dark:text-white">
          {id}
        </h3>
        <button
          onClick={onZoneClick}
          className="p-2 text-gray-600 hover:text-blue-600 dark:text-gray-300 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
        >
          <CgDetailsMore size={24} />
        </button>
      </div>
      <div 
        className="grid grid-cols-2 gap-4"
      >
        {boxes.map((box, index) => (
          <PlantingBox
            key={index}
            name={`Cajón ${index + 1}`}
            envTemp={box.envTemp}
            groundHumidity={box.groundHumidity}
            envHumidity={box.envHumidity}
            status={box.status}
            lastUpdate={new Date()}
          />
        ))}
      </div>
    </div>
  );
} 