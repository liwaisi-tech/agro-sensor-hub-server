# agro-sensor-hub-server
Repositorio para almacenamiento y visualización de datos del los dispositivos ESP32 con sensores de humedad del suelo, temperatura y humedad del ambiente.

## Arquitectura del Sistema

```mermaid
graph TB
    subgraph "IoT Devices"
        ESP[ESP32 Devices]
        S1[Soil Humidity Sensor]
        S2[Temperature Sensor]
        S3[Ambient Humidity Sensor]
        ESP --> S1
        ESP --> S2
        ESP --> S3
    end

    subgraph "Backend Services"
        API[FastAPI REST API]
        BL[Business Logic]
        DB[(PostgreSQL DB)]
        API --> BL
        BL --> DB
    end

    subgraph "Frontend Application"
        RC[React Components]
        RD[Redux State]
        UI[User Interface]
        RC --> RD
        RD --> UI
    end

    ESP -- "HTTP/MQTT" --> API
    UI -- "REST API Calls" --> API

    style ESP32 fill:#f9f,stroke:#333,stroke-width:2px
    style API fill:#bbf,stroke:#333,stroke-width:2px
    style DB fill:#dfd,stroke:#333,stroke-width:2px
    style UI fill:#ffd,stroke:#333,stroke-width:2px
```

### Ejecutar localmente

Para ejecutar este proyecto localmente necesitarás tener instalado `docker compose` en tu equipo. 

copia el archivo `.env.example` y crea un archivo `.env` en este mismo directorio.

Modifica las variables de ambiente para tu base de datos:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=agro_sensor_hub
POSTGRES_HOST=postgres
```

Para iniciar la aplicación en segundo plano con reinicio automático, ejecuta:
```bash
docker compose up -d
```

Este comando:
- `-d`: Ejecuta los contenedores en segundo plano (modo detached)
- Los contenedores se reiniciarán automáticamente si el sistema se reinicia
- Los logs se pueden ver con `docker compose logs -f`

### Ejecutar solo la base de datos

Si necesitas ejecutar solo la base de datos PostgreSQL:
```bash
docker compose up -d postgres
```

