from typing import Optional, List
from sqlalchemy import desc
from sqlalchemy.orm import Session

from domain.models.notification import Notification
from domain.dtos.notification.dtos import NotificationCreate, NotificationResponse


class NotificationRepository:
    def __init__(self):
        pass

    def create(
        self, db: Session, notification_create: NotificationCreate
    ) -> NotificationResponse:
        """
        Create a new notification.

        Args:
            db: Database session
            notification_create: Notification creation data transfer object

        Returns:
            The created Notification record as NotificationResponse
        """
        notification = Notification(
            device_id=notification_create.device_id,
            type=notification_create.type,
            title=notification_create.title,
            description=notification_create.description,
            is_read=False,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return NotificationResponse.model_validate(notification)

    def get_latest_unread(
        self, db: Session, limit: int = 20
    ) -> List[NotificationResponse]:
        """
        Get the latest unread notifications.

        Args:
            db: Database session
            limit: Maximum number of records to return (default 20)

        Returns:
            List of unread Notification records as NotificationResponse
        """
        notifications = (
            db.query(Notification)
            .filter(Notification.is_read == False)
            .order_by(desc(Notification.created_at))
            .limit(limit)
            .all()
        )
        return [
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ]

    def get_paginated(
        self, db: Session, skip: int = 0, limit: int = 10
    ) -> List[NotificationResponse]:
        """
        Get a paginated list of notifications sorted by creation date.

        Args:
            db: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return

        Returns:
            List of Notification records as NotificationResponse
        """
        notifications = (
            db.query(Notification)
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ]

    def update_read_status(
        self, db: Session, notification_id: int, is_read: bool = True
    ) -> Optional[NotificationResponse]:
        """
        Update the read status of a notification.

        Args:
            db: Database session
            notification_id: The ID of the notification
            is_read: The new read status (default True)

        Returns:
            Updated Notification record as NotificationResponse if found, None otherwise
        """
        notification = (
            db.query(Notification).filter(Notification.id == notification_id).first()
        )

        if notification:
            setattr(notification, "is_read", is_read)
            db.commit()
            db.refresh(notification)
            return NotificationResponse.model_validate(notification)

        return None

    def get_by_mac_address(
        self, db: Session, mac_address: str, skip: int = 0, limit: int = 10
    ) -> List[NotificationResponse]:
        """
        Get paginated notifications for a specific MAC address.

        Args:
            db: Database session
            mac_address: The MAC address of the device
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return

        Returns:
            List of Notification records as NotificationResponse for the specified MAC address
        """
        notifications = (
            db.query(Notification)
            .filter(Notification.device_id == mac_address)
            .order_by(desc(Notification.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [
            NotificationResponse.model_validate(notification)
            for notification in notifications
        ]
