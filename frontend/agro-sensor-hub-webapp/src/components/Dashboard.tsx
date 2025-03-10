import { useState } from 'react';
import { Zone as ZoneComponent } from './Zone';
import { Zone } from '../types/zone';
import { mockZones } from '../mocks/zonesData';
import { Modal } from './Modal';
import { ZoneDetail } from './ZoneDetail';

export function Dashboard() {
  const [selectedZone, setSelectedZone] = useState<Zone | null>(null);

  const handleZoneClick = (zone: Zone) => {
    setSelectedZone(zone);
  };

  const handleCloseModal = () => {
    setSelectedZone(null);
  };

  return (
    <>
      <main className="flex-grow bg-gray-100 dark:bg-gray-800 p-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {mockZones.map((zone) => (
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