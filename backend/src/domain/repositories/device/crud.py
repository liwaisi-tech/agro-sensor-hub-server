from typing import Optional, TypedDict

from sqlalchemy.orm import Session

from domain.models.device import Device

class DeviceData(TypedDict):
    """TypedDict for device data."""
    mac_address: str
    device_name: str

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, device_data: DeviceData) -> Device:
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
            mac_address=device_data['mac_address'],
            device_name=device_data['device_name']
        )
        self.db.add(device)
        self.db.commit()
        self.db.refresh(device)
        return device

    def update(self, device_data: DeviceData) -> Optional[Device]:
        """
        Update an existing device record.
        
        Args:
            device_data: Dictionary containing device information
                mac_address: The MAC address of the device to update
                device_name: The new name for the device
            
        Returns:
            Updated Device record if found, None otherwise
        """
        device = self.db.query(Device).filter(Device.mac_address == device_data['mac_address']).first()
        if device:
            device.device_name = device_data['device_name']
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
