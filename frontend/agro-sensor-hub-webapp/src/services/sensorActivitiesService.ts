import { SensorActivity } from '../types/sensorActivity';
import { saveAs } from 'file-saver';

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
    },
    async downloadLastThreeMonths(): Promise<void> {
        const host = window.location.hostname;
        const baseUrl = `http://${host}:8080/agro-sensor-hub/api/v1`;
        const url = `${baseUrl}/sensor-activities/download/last-three-months`;

        try {
            const response = await fetch(url, {
                headers: {
                    'accept': 'text/plain'
                }
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(errorData || 'Error al descargar los datos');
            }

            const blob = await response.blob();
            const currentDate = new Date().toISOString().split('T')[0];
            saveAs(blob, `sensor-data-last-3-months-${currentDate}.csv`);
        } catch (error) {
            console.error('Error downloading CSV:', error);
            throw error;
        }
    }
}; 