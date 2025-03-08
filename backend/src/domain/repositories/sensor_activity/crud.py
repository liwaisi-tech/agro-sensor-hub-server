from datetime import datetime
from typing import Optional, List, TypedDict

from sqlalchemy import desc
from sqlalchemy.orm import Session

from domain.models.sensor_activity import SensorActivity

class SensorActivityData(TypedDict):
    """TypedDict for sensor activity data."""
    mac_address: str
    zone: str
    env_humidity: float
    env_temperature: float
    ground_sensor_1: float
    ground_sensor_2: float
    ground_sensor_3: float
    ground_sensor_4: float
    ground_sensor_5: float
    ground_sensor_6: float

class SensorActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, activity_data: SensorActivityData) -> SensorActivity:
        """
        Create a new sensor activity record.
        
        Args:
            activity_data: Dictionary containing sensor activity information
                mac_address: The MAC address of the device (format: XX:XX:XX:XX:XX:XX)
                zone: The zone where the sensor is located
                env_humidity: Environmental humidity reading
                env_temperature: Environmental temperature reading
                ground_sensor_1: Ground sensor 1 reading
                ground_sensor_2: Ground sensor 2 reading
                ground_sensor_3: Ground sensor 3 reading
                ground_sensor_4: Ground sensor 4 reading
                ground_sensor_5: Ground sensor 5 reading
                ground_sensor_6: Ground sensor 6 reading
            
        Returns:
            The created SensorActivity record
        """
        activity = SensorActivity(
            mac_address=activity_data['mac_address'],
            zone=activity_data['zone'],
            env_humidity=activity_data['env_humidity'],
            env_temperature=activity_data['env_temperature'],
            ground_sensor_1=activity_data['ground_sensor_1'],
            ground_sensor_2=activity_data['ground_sensor_2'],
            ground_sensor_3=activity_data['ground_sensor_3'],
            ground_sensor_4=activity_data['ground_sensor_4'],
            ground_sensor_5=activity_data['ground_sensor_5'],
            ground_sensor_6=activity_data['ground_sensor_6']
        )
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_filtered_list(
        self,
        skip: int = 0,
        limit: int = 10,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[SensorActivity]:
        """
        Get a filtered and paginated list of sensor activities.
        
        Args:
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of SensorActivity records
        """
        query = self.db.query(SensorActivity)
        
        if start_date:
            query = query.filter(SensorActivity.created_at >= start_date)
        if end_date:
            query = query.filter(SensorActivity.created_at <= end_date)
            
        return query.order_by(desc(SensorActivity.created_at)).offset(skip).limit(limit).all()

    def get_by_id(self, activity_id: int) -> Optional[SensorActivity]:
        """
        Get a sensor activity record by its ID.
        
        Args:
            activity_id: The ID of the sensor activity record
            
        Returns:
            SensorActivity record if found, None otherwise
        """
        return self.db.query(SensorActivity).filter(SensorActivity.id == activity_id).first()

    def get_latest_by_mac_address(self, mac_address: str) -> Optional[SensorActivity]:
        """
        Get the latest sensor activity record for a specific MAC address.
        
        Args:
            mac_address: The MAC address of the sensor
            
        Returns:
            Most recent SensorActivity record for the MAC address if found, None otherwise
        """
        return (
            self.db.query(SensorActivity)
            .filter(SensorActivity.mac_address == mac_address)
            .order_by(desc(SensorActivity.created_at))
            .first()
        )
    