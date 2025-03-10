from datetime import datetime
from typing import Optional, List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.repositories.sensor_activity.crud import SensorActivityRepository
from domain.dtos.sensor_activity.dtos import (
    SensorActivityCreate,
    SensorActivityResponse,
)
from application.services.device.services import DeviceService
from domain.dtos.device.dtos import DeviceCreate, DeviceResponse


class SensorActivityService:
    """Service class for handling sensor activity operations."""

    def __init__(
        self,
        sensor_activity_repository: SensorActivityRepository,
        device_service: DeviceService,
    ):
        self.repository = sensor_activity_repository
        self.device_service = device_service

    def _ensure_device_exists(
        self, db: Session, mac_address: str, zone: Optional[str]
    ) -> DeviceResponse:
        """
        Ensures a device exists in the system. Creates it if it doesn't exist.

        Args:
            db: Database session
            mac_address: Device MAC address
            zone: Optional zone name to use as device name

        Returns:
            DeviceResponse: The existing or newly created device
        """
        try:
            return self.device_service.get_device_by_mac_address(db, mac_address)
        except HTTPException as he:
            if he.status_code == 404:
                device_name = zone if zone else mac_address
                device_create = DeviceCreate(mac_address=mac_address, name=device_name)
                return self.device_service.create_device(db, device_create)
            raise he

    def _update_device_zone(
        self, db: Session, device: DeviceResponse, new_zone: str
    ) -> None:
        """
        Updates device name with new zone if different.

        Args:
            db: Database session
            device: Current device information
            new_zone: New zone name to set
        """
        if device.name != new_zone:
            self.device_service.update_device(
                db, DeviceCreate(mac_address=device.mac_address, name=new_zone)
            )

    def create(
        self, db: Session, activity_create: SensorActivityCreate
    ) -> SensorActivityResponse:
        """
        Create a new sensor activity record. If the device doesn't exist, it will be created.
        If the device exists and has a different zone name, it will be updated.

        Args:
            db: Database session
            activity_create: Sensor activity creation data transfer object

        Returns:
            The created SensorActivity record with device information

        Raises:
            HTTPException: If there's an error creating the sensor activity
        """
        try:
            # Step 1: Ensure device exists
            device = self._ensure_device_exists(
                db, activity_create.mac_address, activity_create.zone
            )

            # Step 2: Update device zone if needed
            if activity_create.zone:
                self._update_device_zone(db, device, activity_create.zone)

            # Step 3: Create sensor activity record
            return self.repository.create(db, activity_create)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating sensor activity: {str(e)}"
            )

    def get_filtered_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[SensorActivityResponse]:
        """
        Get a filtered and paginated list of sensor activities.

        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            List of SensorActivity records

        Raises:
            HTTPException: If there's an error retrieving the sensor activities
        """
        try:
            activities = self.repository.get_filtered_list(
                db=db, skip=skip, limit=limit, start_date=start_date, end_date=end_date
            )
            if not activities:
                raise HTTPException(
                    status_code=404, detail="No sensor activities found"
                )
            return activities
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving sensor activities: {str(e)}"
            )

    def get_by_id(self, db: Session, activity_id: int) -> SensorActivityResponse:
        """
        Get a sensor activity record by its ID.

        Args:
            db: Database session
            activity_id: The ID of the sensor activity record

        Returns:
            SensorActivity record if found

        Raises:
            HTTPException: If the activity is not found or if there's an error retrieving it
        """
        try:
            activity = self.repository.get_by_id(db, activity_id)
            if not activity:
                raise HTTPException(
                    status_code=404,
                    detail=f"Sensor activity with id {activity_id} not found",
                )
            return activity
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving sensor activity: {str(e)}"
            )

    def get_latest_by_mac_address(
        self, db: Session, mac_address: str
    ) -> SensorActivityResponse:
        """
        Get the latest sensor activity record for a specific MAC address.

        Args:
            db: Database session
            mac_address: The MAC address of the sensor

        Returns:
            Most recent SensorActivity record for the MAC address

        Raises:
            HTTPException: If no activity is found for the MAC address or if there's an error retrieving it
        """
        try:
            activity = self.repository.get_latest_by_mac_address(db, mac_address)
            if not activity:
                raise HTTPException(
                    status_code=404,
                    detail=f"No sensor activity found for device with MAC address {mac_address}",
                )
            return activity
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving latest sensor activity: {str(e)}",
            )
