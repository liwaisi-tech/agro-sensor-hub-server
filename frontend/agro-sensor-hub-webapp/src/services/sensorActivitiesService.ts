import { SensorActivity } from '../types/sensorActivity';

interface ApiError {
    detail: string;
}

export const sensorActivitiesService = {
    async getActivities(params: {
        currentPage: number;
        itemsPerPage: number;
        startDate?: Date;
        endDate?: Date;
    }): Promise<{ activities: SensorActivity[]; hasNextPage: boolean }> {
        const host = window.location.hostname;
        const baseUrl = `http://${host}:8080/agro-sensor-hub/api/v1`;

        let url = `${baseUrl}/sensor-activities?skip=${params.currentPage * params.itemsPerPage}&limit=${params.itemsPerPage + 1}`;

        if (params.startDate) {
            url += `&start_date=${params.startDate.toISOString()}`;
        }
        if (params.endDate) {
            url += `&end_date=${params.endDate.toISOString()}`;
        }

        const response = await fetch(url, {
            headers: {
                'accept': 'application/json'
            }
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error((data as ApiError).detail || 'Network response was not ok');
        }

        if (!Array.isArray(data)) {
            throw new Error('No se encontraron datos para los filtros seleccionados');
        }

        return {
            activities: data.slice(0, params.itemsPerPage),
            hasNextPage: data.length > params.itemsPerPage
        };
    }
}; 