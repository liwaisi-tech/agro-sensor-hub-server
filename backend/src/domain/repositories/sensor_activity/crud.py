from datetime import datetime
from typing import Optional, List
from sqlalchemy import desc, func
from sqlalchemy.orm import Session, joinedload

from domain.models.sensor_activity import SensorActivity
from domain.dtos.sensor_activity.dtos import (
    SensorActivityCreate,
    SensorActivityResponse,
)


class SensorActivityRepository:
    def __init__(self):
        pass

    def create(
        self, db: Session, activity_create: SensorActivityCreate
    ) -> SensorActivityResponse:
        """
        Create a new sensor activity record.

        Args:
            db: Database session
            activity_create: Sensor activity creation data transfer object

        Returns:
            The created SensorActivity record as SensorActivityResponse
        """
        activity = SensorActivity(
            device_id=activity_create.mac_address,
            zone=activity_create.zone,
            env_humidity=activity_create.env_humidity,
            env_temperature=activity_create.env_temperature,
            ground_sensor_1=activity_create.ground_sensor_1,
            ground_sensor_2=activity_create.ground_sensor_2,
            ground_sensor_3=activity_create.ground_sensor_3,
            ground_sensor_4=activity_create.ground_sensor_4,
            ground_sensor_5=activity_create.ground_sensor_5,
            ground_sensor_6=activity_create.ground_sensor_6,
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)

        # Reload with device information
        activity = (
            db.query(SensorActivity)
            .options(joinedload(SensorActivity.device))
            .filter(SensorActivity.id == activity.id)
            .first()
        )

        return SensorActivityResponse.model_validate(activity)

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
            List of SensorActivity records as SensorActivityResponse
        """
        query = db.query(SensorActivity).options(joinedload(SensorActivity.device))

        if start_date:
            query = query.filter(SensorActivity.created_at >= start_date)
        if end_date:
            query = query.filter(SensorActivity.created_at <= end_date)

        activities = (
            query.order_by(desc(SensorActivity.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            SensorActivityResponse.model_validate(activity) for activity in activities
        ]

    def get_by_id(
        self, db: Session, activity_id: int
    ) -> Optional[SensorActivityResponse]:
        """
        Get a sensor activity record by its ID.

        Args:
            db: Database session
            activity_id: The ID of the sensor activity record

        Returns:
            SensorActivity record as SensorActivityResponse if found, None otherwise
        """
        activity = (
            db.query(SensorActivity)
            .options(joinedload(SensorActivity.device))
            .filter(SensorActivity.id == activity_id)
            .first()
        )
        return SensorActivityResponse.model_validate(activity) if activity else None

    def get_latest_by_mac_address(
        self, db: Session, mac_address: str
    ) -> Optional[SensorActivityResponse]:
        """
        Get the latest sensor activity record for a specific MAC address.

        Args:
            db: Database session
            mac_address: The MAC address of the sensor

        Returns:
            Most recent SensorActivity record as SensorActivityResponse for the MAC address if found, None otherwise
        """
        activity = (
            db.query(SensorActivity)
            .options(joinedload(SensorActivity.device))
            .filter(SensorActivity.device_id == mac_address)
            .order_by(desc(SensorActivity.created_at))
            .first()
        )
        return SensorActivityResponse.model_validate(activity) if activity else None

    def get_latest_for_all_devices(self, db: Session) -> List[SensorActivityResponse]:
        """
        Get the latest sensor activity record for each unique device.
        Returns only one record per device (the most recent one).
        """
        # Subquery to get the latest record ID for each device
        latest_ids = (
            db.query(
                SensorActivity.device_id,
                func.max(SensorActivity.id).label('latest_id')
            )
            .group_by(SensorActivity.device_id)
            .subquery()
        )

        # Main query joining with the subquery to get the full records
        activities = (
            db.query(SensorActivity)
            .options(joinedload(SensorActivity.device))
            .join(
                latest_ids,
                SensorActivity.device_id == latest_ids.c.device_id
            )
            .filter(SensorActivity.id == latest_ids.c.latest_id)
            .order_by(desc(SensorActivity.created_at))
            .all()
        )
        return [
            SensorActivityResponse.model_validate(activity) for activity in activities
        ]
