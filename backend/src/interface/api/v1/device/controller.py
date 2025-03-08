from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from application.services.device.services import DeviceService
from infrastructure.database.base import get_db

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

@router.post(
    "",
    response_model=DeviceResponse,
    summary="Create new device",
    description="Creates a new device in the system"
)
async def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(DeviceService)
) -> DeviceResponse:
    """
    Creates a new device in the system.
    
    Args:
        device: Device creation data transfer object
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        DeviceResponse: The created device data
    """
    return device_service.create_device(db, device)

@router.put(
    "",
    response_model=DeviceResponse,
    summary="Update existing device",
    description="Updates an existing device in the system"
)
async def update_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(DeviceService)
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
    return device_service.update_device(db, device)

@router.get(
    "/{mac_address}",
    response_model=DeviceResponse,
    summary="Get device by MAC address",
    description="Retrieves a device by its MAC address"
)
async def get_device_by_mac_address(
    mac_address: str,
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(DeviceService)
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
    return device_service.get_device_by_mac_address(db, mac_address)

@router.get(
    "",
    response_model=List[DeviceResponse],
    summary="Get all devices",
    description="Retrieves all devices in the system"
)
async def get_all_devices(
    db: Session = Depends(get_db),
    device_service: DeviceService = Depends(DeviceService)
) -> List[DeviceResponse]:
    """
    Retrieves all devices in the system.
    
    Args:
        db: Database session
        device_service: Service that handles device operations
    
    Returns:
        List[DeviceResponse]: List of all devices
    """
    return device_service.get_all_devices(db) 