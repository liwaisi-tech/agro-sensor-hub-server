from typing import Optional, TypedDict, List

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
            The created Device record as DeviceResponse
        """
        device = Device(
            mac_address=device_create.mac_address, name=str(device_create.name)
        )
        db.add(device)
        db.commit()
        db.refresh(device)
        return DeviceResponse.model_validate(device)

    def update(
        self, db: Session, device_create: DeviceCreate
    ) -> Optional[DeviceResponse]:
        """
        Update an existing device record.

        Args:
            db: Database session
            device_create: Device creation data transfer object

        Returns:
            Updated Device record as DeviceResponse if found, None otherwise
        """
        device = (
            db.query(Device)
            .filter(Device.mac_address == device_create.mac_address)
            .first()
        )
        if device:
            setattr(device, "name", str(device_create.name))
            db.commit()
            db.refresh(device)
            return DeviceResponse.model_validate(device)
        return None

    def get_by_mac_address(
        self, db: Session, mac_address: str
    ) -> Optional[DeviceResponse]:
        """
        Get a device by its MAC address.

        Args:
            db: Database session
            mac_address: The MAC address of the device to retrieve

        Returns:
            Device record as DeviceResponse if found, None otherwise
        """
        device = db.query(Device).filter(Device.mac_address == mac_address).first()
        return DeviceResponse.model_validate(device) if device else None

    def get_all_devices(self, db: Session) -> List[DeviceResponse]:
        """
        Get all devices sorted by name.

        Args:
            db: Database session

        Returns:
            List of Device records as DeviceResponse sorted alphabetically by name
        """
        devices = db.query(Device).order_by(Device.name).all()
        return [DeviceResponse.model_validate(device) for device in devices]
