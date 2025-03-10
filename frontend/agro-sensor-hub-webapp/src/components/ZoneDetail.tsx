import { PlantingBox } from './PlantingBox'
import { Zone } from '../types/zone'

interface ZoneDetailProps {
  zone: Zone;
}

export function ZoneDetail({ zone }: ZoneDetailProps) {
  return (
    <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4">
      <div className="container mx-auto">
        <div className="bg-white dark:bg-gray-700 rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-2">{zone.name}</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-2">Detalle de la {zone.name}</p>
          <p className="text-gray-600 dark:text-gray-300 mb-2">Dispositivo: {zone.mac_address}</p>
          <p className="text-gray-600 dark:text-gray-300 mb-6">Última lectura: {new Date(zone.latest_reading).toLocaleString('es-CO')}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {zone.planting_boxes.map((box, index) => (
              <PlantingBox
                key={index}
                name={box.name}
                envTemp={zone.environment_temperature}
                groundHumidity={box.ground_humidity}
                envHumidity={zone.environment_humidity}
                status={zone.status}
                lastUpdate={new Date(zone.latest_reading)}
              />
            ))}
          </div>
        </div>
      </div>
    </main>
  )
} 