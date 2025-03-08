from typing import List
from fastapi import HTTPException
from domain.dtos.device.dtos import DeviceCreate, DeviceResponse
from domain.repositories.device.crud import DeviceRepository


class DeviceService:
    def __init__(self, device_repository: DeviceRepository):
        self.device_repository = device_repository

    def create_device(self, device: DeviceCreate) -> DeviceResponse:
        if self.device_repository.get_by_mac_address(device.mac_address):
            raise HTTPException(status_code=400, detail="Device already exists")
        if device.name is None:
            device.name = device.mac_address
        return self.device_repository.create(device)
    
    def update_device(self, device: DeviceCreate) -> DeviceResponse:
        if not self.device_repository.get_by_mac_address(device.mac_address):
            raise HTTPException(status_code=404, detail="Device not found")
        if device.name is None:
            device.name = device.mac_address
        return self.device_repository.update(device)
    
    def get_device_by_mac_address(self, mac_address: str) -> DeviceResponse:
        device = self.device_repository.get_by_mac_address(mac_address)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    
    def get_all_devices(self) -> List[DeviceResponse]:
        """
        Get all devices sorted by name.
        
        Returns:
            List of Device records sorted alphabetically by name
        """
        devices = self.device_repository.get_all_devices()
        if len(devices) == 0:
            raise HTTPException(status_code=404, detail="No devices found")
        return [DeviceResponse.model_validate(device) for device in devices]
    