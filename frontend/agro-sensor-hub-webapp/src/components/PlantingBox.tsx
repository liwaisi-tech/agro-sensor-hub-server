import { CgThermometer, CgDropOpacity, CgCloud, CgTime, CgClose } from "react-icons/cg";
import { useEffect, useState } from 'react';
import { getRelativeTimeString } from '../utils/dateUtils';

interface PlantingBoxProps {
  name: string;
  envTemp: number;
  groundHumidity: number;
  envHumidity: number;
  status: "active" | "inactive";
  lastUpdate?: Date;
}

export function PlantingBox({ 
  name,
  envTemp, 
  groundHumidity, 
  envHumidity, 
  status,
  lastUpdate = new Date()
}: PlantingBoxProps) {
  const [relativeTime, setRelativeTime] = useState<string>(getRelativeTimeString(lastUpdate));

  useEffect(() => {
    // Update the relative time every minute
    const interval = setInterval(() => {
      setRelativeTime(getRelativeTimeString(lastUpdate));
    }, 60000);

    return () => clearInterval(interval);
  }, [lastUpdate]);

  // Don't render the box if ground humidity is 0
  if (groundHumidity === 0) {
    return null;
  }

  return (
    <div className={`w-38 h-38 rounded-lg p-4 ${
      status === "active" 
        ? 'bg-green-500 dark:bg-green-600' 
        : 'bg-red-500 dark:bg-red-600'
    } text-white shadow-md flex flex-col justify-between`}>
      <div className="flex flex-col gap-2">
        <h3 className="text-sm font-semibold text-white/90">{name}</h3>
        <div className="flex items-center">
          <div className="flex items-center gap-1">
            <CgThermometer className="text-xl text-amber-200 dark:text-amber-300" />
            <span className="text-xs text-white">Temp</span>
          </div>
          {envTemp === 0 ? (
            <CgClose className="text-sm text-white/60 ml-2" />
          ) : (
            <span className="text-sm text-white font-bold ml-2">{envTemp}°C</span>
          )}
        </div>        
        <div className="flex items-center">
          <div className="flex items-center gap-1">
            <CgCloud className="text-xl text-blue-100 dark:text-blue-200" />
            <span className="text-xs text-white">Aire</span>
          </div>
          {envHumidity === 0 ? (
            <CgClose className="text-sm text-white/60 ml-2" />
          ) : (
            <span className="text-sm text-white font-bold ml-2">{envHumidity}%</span>
          )}
        </div>
        <div className="flex items-center">
          <div className="flex items-center gap-1">
            <CgDropOpacity className="text-xl text-blue-100 dark:text-blue-200" />
            <span className="text-xs text-white">Suelo</span>
          </div>
          {groundHumidity === 0 ? (
            <CgClose className="text-sm text-white/60 ml-2" />
          ) : (
            <span className="text-sm text-white font-bold ml-2">{groundHumidity}%</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-1 mt-2 border-t border-white/10 pt-2">
        <CgTime className="text-xs text-white/60" />
        <span className="text-[10px] text-white/60">{relativeTime}</span>
      </div>
    </div>
  );
} 