from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from application.services.device.services import DeviceService
from domain.repositories.device.crud import DeviceRepository
from infrastructure.database.base import get_db
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

def get_device_service() -> DeviceService:
    """
    Dependency provider for DeviceService.
    
    Returns:
        DeviceService: An instance of the device service
    """
    return DeviceService(DeviceRepository())

@router.post(
    "",
    response_model=DeviceResponse,
    summary="Create new device",
    description="Creates a new device in the system with the specified MAC address. The device name is optional.",
    status_code=201,
    responses={
        201: {"description": "Device created successfully"},
        400: {"description": "Device already exists"},
        422: {"description": "Validation Error - Invalid MAC address format"}
    }
)
async def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(get_device_service)
) -> DeviceResponse:
    """
    Creates a new device in the system.
    
    Args:
        device: Device creation data transfer object containing:
            - mac_address: The MAC address of the device (required, format: XX:XX:XX:XX:XX:XX)
            - name: Optional friendly name for the device
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        DeviceResponse: The created device data including creation timestamp
        
    Raises:
        HTTPException: 400 if device already exists
        HTTPException: 422 if MAC address format is invalid
    """
    logger.info(f"Creating new device with MAC address: {device.mac_address}")
    response = device_service.create_device(db, device)
    logger.info(f"Device created successfully: {response}")
    return response

@router.put(
    "",
    response_model=DeviceResponse,
    summary="Update existing device",
    description="Updates an existing device in the system"
)
async def update_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(get_device_service)
) -> DeviceResponse:
    """
    Updates an existing device in the system.
    
    Args:
        device: Device update data transfer object
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        DeviceResponse: The updated device data
    """
    logger.info(f"Updating device with MAC address: {device.mac_address}")
    response = device_service.update_device(db, device)
    logger.info(f"Device updated successfully: {response}")
    return response

@router.get(
    "/{mac_address}",
    response_model=DeviceResponse,
    summary="Get device by MAC address",
    description="Retrieves a device by its MAC address"
)
async def get_device_by_mac_address(
    mac_address: str,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(get_device_service)
) -> DeviceResponse:
    """
    Retrieves a device by its MAC address.
    
    Args:
        mac_address: The MAC address of the device
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        DeviceResponse: The device data
    """
    logger.info(f"Retrieving device with MAC address: {mac_address}")
    response = device_service.get_device_by_mac_address(db, mac_address)
    logger.info(f"Device retrieved successfully: {response}")
    return response

@router.get(
    "",
    response_model=List[DeviceResponse],
    summary="Get all devices",
    description="Retrieves all devices in the system"
)
async def get_all_devices(
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(get_device_service)
) -> List[DeviceResponse]:
    """
    Retrieves all devices in the system.
    
    Args:
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        List[DeviceResponse]: List of all devices
    """
    logger.info("Retrieving all devices")
    response = device_service.get_all_devices(db)
    logger.info(f"Retrieved {len(response)} devices successfully")
    return response 