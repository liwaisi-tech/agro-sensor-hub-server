from datetime import datetime
import fastapi
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from domain.dtos.sensor_activity.dtos import (
    SensorActivityCreate,
    SensorActivityListResponse,
    SensorActivityResponse,
)
from application.services.sensor_activity.services import SensorActivityService
from domain.repositories.sensor_activity.crud import SensorActivityRepository
from application.services.device.services import DeviceService
from domain.repositories.device.crud import DeviceRepository
from infrastructure.database.base import get_db
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/sensor-activities", tags=["Sensor Activities"])


def get_sensor_activity_service() -> SensorActivityService:
    """
    Dependency provider for SensorActivityService.

    Returns:
        SensorActivityService: An instance of the sensor activity service
    """
    return SensorActivityService(
        sensor_activity_repository=SensorActivityRepository(),
        device_service=DeviceService(DeviceRepository()),
    )


@router.post(
    "",
    response_model=SensorActivityResponse,
    summary="Create new sensor activity",
    description="Records a new sensor activity reading from a device",
    status_code=201,
    responses={
        201: {"description": "Sensor activity recorded successfully"},
        422: {"description": "Validation Error - Invalid data format"},
        500: {"description": "Internal server error"},
    },
)
async def create_sensor_activity(
    activity: SensorActivityCreate,
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> SensorActivityResponse:
    """
    Records a new sensor activity reading.

    Args:
        activity: Sensor activity data transfer object containing:
            - mac_address: The MAC address of the device (required, format: XX:XX:XX:XX:XX:XX)
            - zone: Optional zone identifier
            - env_humidity: Optional environmental humidity reading
            - env_temperature: Optional environmental temperature reading
            - ground_sensor_1 through ground_sensor_6: Optional ground sensor readings
        db: Database session
        sensor_activity_service: Service that handles sensor activity operations

    Returns:
        SensorActivityResponse: The recorded sensor activity data including creation timestamp

    Raises:
        HTTPException: 422 if data format is invalid
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Recording new sensor activity for device: {activity.mac_address}")
    response = sensor_activity_service.create(db, activity)
    logger.info(f"Sensor activity recorded successfully: {response}")
    return response


@router.get(
    "",
    response_model=List[SensorActivityResponse],
    summary="Get filtered sensor activities",
    description="Retrieves a filtered and paginated list of sensor activities",
)
async def get_sensor_activities(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        10, ge=1, le=100, description="Maximum number of records to return"
    ),
    start_date: Optional[datetime] = Query(
        None, description="Filter activities from this date"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter activities until this date"
    ),
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> List[SensorActivityResponse]:
    """
    Retrieves a filtered list of sensor activities.

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        start_date: Optional start date filter
        end_date: Optional end date filter
        db: Database session
        sensor_activity_service: Service that handles sensor activity operations

    Returns:
        List[SensorActivityResponse]: List of sensor activities matching the criteria

    Raises:
        HTTPException: 404 if no activities found
        HTTPException: 500 if there's a server error
    """
    logger.info(
        f"Retrieving sensor activities with filters: skip={skip}, limit={limit}, start_date={start_date}, end_date={end_date}"
    )
    response = sensor_activity_service.get_filtered_list(
        db, skip, limit, start_date, end_date
    )
    logger.info(f"Retrieved {len(response)} sensor activities successfully")
    return response


@router.get(
    "/{activity_id}",
    response_model=SensorActivityResponse,
    summary="Get sensor activity by ID",
    description="Retrieves a specific sensor activity by its ID",
)
async def get_sensor_activity_by_id(
    activity_id: int,
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> SensorActivityResponse:
    """
    Retrieves a specific sensor activity by its ID.

    Args:
        activity_id: The ID of the sensor activity record
        db: Database session
        sensor_activity_service: Service that handles sensor activity operations

    Returns:
        SensorActivityResponse: The sensor activity data

    Raises:
        HTTPException: 404 if activity not found
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Retrieving sensor activity with ID: {activity_id}")
    response = sensor_activity_service.get_by_id(db, activity_id)
    logger.info(f"Sensor activity retrieved successfully: {response}")
    return response


@router.get(
    "/device/{mac_address}/latest",
    response_model=SensorActivityResponse,
    summary="Get latest sensor activity for device",
    description="Retrieves the most recent sensor activity for a specific device",
)
async def get_latest_sensor_activity(
    mac_address: str,
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> SensorActivityResponse:
    """
    Retrieves the most recent sensor activity for a specific device.

    Args:
        mac_address: The MAC address of the device
        db: Database session
        sensor_activity_service: Service that handles sensor activity operations

    Returns:
        SensorActivityResponse: The most recent sensor activity data for the device

    Raises:
        HTTPException: 404 if no activity found for the device
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Retrieving latest sensor activity for device: {mac_address}")
    response = sensor_activity_service.get_latest_by_mac_address(db, mac_address)
    logger.info(f"Latest sensor activity retrieved successfully: {response}")
    return response


@router.get(
    "/all/latest",
    response_model=List[SensorActivityListResponse],
    summary="Get latest sensor activity for all devices",
)
async def get_latest_sensor_activity_for_all_devices(
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> List[SensorActivityListResponse]:
    """
    Retrieves the latest sensor activity for all devices.
    """
    logger.info("Retrieving latest sensor activity for all devices")
    response = sensor_activity_service.get_latest_for_all_devices(db)
    logger.info(f"Latest sensor activity retrieved successfully: {response}")
    return response


@router.get(
    "/download/last-three-months",
    response_class=fastapi.responses.PlainTextResponse,
    summary="Download sensor activity data for the last three months as CSV",
    description="Downloads a CSV file containing all sensor activity data from the last three months",
    responses={
        200: {"description": "CSV file with sensor activity data"},
        404: {"description": "No sensor activities found in the last three months"},
        500: {"description": "Internal server error"},
    },
)
async def download_last_three_months_csv(
    db: Session = Depends(get_db),
    sensor_activity_service: SensorActivityService = Depends(
        get_sensor_activity_service
    ),
) -> fastapi.responses.PlainTextResponse:
    """
    Downloads a CSV file containing all sensor activity data from the last three months.
    
    Args:
        db: Database session
        sensor_activity_service: Service that handles sensor activity operations
        
    Returns:
        PlainTextResponse: CSV file with sensor activity data
        
    Raises:
        HTTPException: 404 if no activities found in the last three months
        HTTPException: 500 if there's a server error
    """
    logger.info("Generating CSV download for the last three months of sensor activity data")
    csv_content = sensor_activity_service.get_last_three_months_csv(db)
    
    # Create a response with the CSV content and appropriate headers
    response = fastapi.responses.PlainTextResponse(
        content=csv_content,
        media_type="text/csv"
    )
    
    # Set headers for file download
    filename = f"sensor_activity_data_{datetime.now().strftime('%Y%m%d')}.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    
    logger.info(f"CSV download generated successfully: {filename}")
    return response
