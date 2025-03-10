import { useState, useEffect } from 'react';
import { Zone as ZoneComponent } from './Zone';
import { Zone } from '../types/zone';
import { Modal } from './Modal';
import { ZoneDetail } from './ZoneDetail';
import { zonesService } from '../services/zonesService';
import { CgLoadbar } from 'react-icons/cg';

export function Dashboard() {
  const [selectedZone, setSelectedZone] = useState<Zone | null>(null);
  const [zones, setZones] = useState<Zone[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchZones = async () => {
      try {
        setIsLoading(true);
        const data = await zonesService.getAllZones();
        setZones(data);
      } catch (err) {
        setError('No se pudieron cargar las zonas');
        console.error('Error loading zones:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchZones();
  }, []);

  const handleZoneClick = (zone: Zone) => {
    setSelectedZone(zone);
  };

  const handleCloseModal = () => {
    setSelectedZone(null);
  };

  if (isLoading) {
    return (
      <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-300">Cargando información...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4 flex items-center justify-center">
        <div className="text-xl text-red-500">{error}</div>
      </main>
    );
  }

  if (zones.length === 0) {
    return (
      <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4 flex items-center justify-center">
        <div className="text-xl text-gray-600 dark:text-gray-300">No se encontraron lecturas recientes</div>
      </main>
    );
  }

  return (
    <>
      <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Bienvenido al Panel de Control</h1>
          <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-300">
            <div className="flex items-center gap-2">
              <CgLoadbar className="text-green-500 text-xl" />
              <span>Datos actualizados (últimos 10 minutos)</span>
            </div>
            <div className="flex items-center gap-2">
              <CgLoadbar className="text-red-500 text-xl" />
              <span>Datos desactualizados (más de 10 minutos)</span>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {zones.map((zone: Zone) => (
            <ZoneComponent
              key={zone.mac_address}
              id={zone.name}
              boxes={zone.planting_boxes.map((box) => ({
                envTemp: zone.environment_temperature,
                groundHumidity: box.ground_humidity,
                envHumidity: zone.environment_humidity,
                status: zone.status
              }))}
              onZoneClick={() => handleZoneClick(zone)}
              latestLecture={zone.latest_reading}
            />
          ))}
        </div>
      </main>

      {selectedZone && (
        <Modal onClose={handleCloseModal}>
          <ZoneDetail zone={selectedZone} />
        </Modal>
      )}
    </>
  );
} 