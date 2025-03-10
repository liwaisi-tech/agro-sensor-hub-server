export interface PlantingBox {
    name: string;
    ground_humidity: number;
}

export interface Zone {
    mac_address: string;
    name: string;
    status: "active" | "inactive";
    environment_temperature: number;
    environment_humidity: number;
    planting_boxes: PlantingBox[];
    latest_reading: string; // ISO timestamp
}