from typing import Optional, TypedDict

from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from sqlalchemy.orm import Session

from domain.models.device import Device

class DeviceData(TypedDict):
    """TypedDict for device data."""
    mac_address: str
    device_name: str

class DeviceRepository:
    def __init__(self):
        pass

    def create(self, db: Session, device_create: DeviceCreate) -> DeviceResponse:
        """
        Create a new device record.
        
        Args:
            db: Database session
            device_create: Device creation data transfer object
            
        Returns:
            The created Device record
        """
        device = Device(
            mac_address=device_create.mac_address,
            name=str(device_create.name)
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def update(self, db: Session, device_create: DeviceCreate) -> Optional[Device]:
        """
        Update an existing device record.
        
        Args:
            db: Database session
            device_create: Device creation data transfer object
            
        Returns:
            Updated Device record if found, None otherwise
        """
        device = db.query(Device).filter(Device.mac_address == device_create.mac_address).first()
        if device:
            setattr(device, 'name', str(device_create.name))
            db.commit()
            db.refresh(device)
        return device

    def get_by_mac_address(self, db: Session, mac_address: str) -> Optional[Device]:
        """
        Get a device by its MAC address.
        
        Args:
            db: Database session
            mac_address: The MAC address of the device to retrieve
            
        Returns:
            Device record if found, None otherwise
        """
        return db.query(Device).filter(Device.mac_address == mac_address).first()

    def get_all_devices(self, db: Session) -> list[Device]:
        """
        Get all devices sorted by name.
        
        Args:
            db: Database session
            
        Returns:
            List of Device records sorted alphabetically by name
        """
        return db.query(Device).order_by(Device.name).all()
