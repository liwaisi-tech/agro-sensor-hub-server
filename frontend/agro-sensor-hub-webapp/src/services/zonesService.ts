import { Zone } from '../types/zone';

export const zonesService = {
    async getAllZones(): Promise<Zone[]> {
        const host = window.location.hostname;
        const baseUrl = `http://${host}:8080/agro-sensor-hub/api/v1`;

        const response = await fetch(`${baseUrl}/sensor-activities/all/latest`, {
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