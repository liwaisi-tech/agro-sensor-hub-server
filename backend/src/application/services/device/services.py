from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from domain.repositories.device.crud import DeviceRepository


class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def create_device(self, db: Session, device: DeviceCreate) -> DeviceResponse:
        try:
            if self.device_repository.get_by_mac_address(db, device.mac_address):
                raise HTTPException(status_code=400, detail="Device already exists")
            if device.name is None:
                device.name = device.mac_address
            return self.device_repository.create(db, device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def update_device(self, db: Session, device: DeviceCreate) -> DeviceResponse:
        if not self.device_repository.get_by_mac_address(db, device.mac_address):
            raise HTTPException(status_code=404, detail="Device not found")
        if device.name is None:
            device.name = device.mac_address
        return self.device_repository.update(db, device)
    
    def get_device_by_mac_address(self, db: Session, mac_address: str) -> DeviceResponse:
        device = self.device_repository.get_by_mac_address(db, mac_address)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    
    def get_all_devices(self, db: Session) -> List[DeviceResponse]:
        """
        Get all devices sorted by name.
        
        Args:
            db: Database session
            
        Returns:
            List of Device records sorted alphabetically by name
        """
        devices = self.device_repository.get_all_devices(db)
        if len(devices) == 0:
            raise HTTPException(status_code=404, detail="No devices found")
        return [DeviceResponse.model_validate(device) for device in devices]
    