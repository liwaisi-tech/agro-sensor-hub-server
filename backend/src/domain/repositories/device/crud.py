from typing import Optional, TypedDict

from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from sqlalchemy.orm import Session

from domain.models.device import Device

class DeviceData(TypedDict):
    """TypedDict for device data."""
    mac_address: str
    device_name: str

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, device_create: DeviceCreate) -> DeviceResponse:
        """
        Create a new device record.
        
        Args:
            device_data: Dictionary containing device information
                mac_address: The MAC address of the device (format: XX:XX:XX:XX:XX:XX)
                device_name: The name of the device
            
        Returns:
            The created Device record
        """
        device = Device(
            mac_address=device_create.mac_address,
            name=str(device_create.name)
        )
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update(self, device_create: DeviceCreate) -> Optional[Device]:
        """
        Update an existing device record.
        
        Args:
            device_data: Dictionary containing device information
                mac_address: The MAC address of the device to update
                device_name: The new name for the device
            
        Returns:
            Updated Device record if found, None otherwise
        """
        device = self.db.query(Device).filter(Device.mac_address == device_create.mac_address).first()
        if device:
            setattr(device, 'name', str(device_create.name))
            self.db.commit()
            self.db.refresh(device)
        return device

    def get_by_mac_address(self, mac_address: str) -> Optional[Device]:
        """
        Get a device by its MAC address.
        
        Args:
            mac_address: The MAC address of the device to retrieve
            
        Returns:
            Device record if found, None otherwise
        """
        return self.db.query(Device).filter(Device.mac_address == mac_address).first()

    def get_all_devices(self) -> list[Device]:
        """
        Get all devices sorted by name.
        
        Returns:
            List of Device records sorted alphabetically by name
        """
        return self.db.query(Device).order_by(Device.name).all()
