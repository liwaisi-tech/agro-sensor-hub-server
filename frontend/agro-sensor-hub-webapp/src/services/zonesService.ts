import { Zone } from '../types/zone';

const API_BASE_URL = 'http://0.0.0.0:8080/agro-sensor-hub/api/v1';

export const zonesService = {
    async getAllZones(): Promise<Zone[]> {
        const response = await fetch(`${API_BASE_URL}/sensor-activities/all/latest`, {
            headers: {
                'accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch zones');
        }

        return response.json();
    }
}; 