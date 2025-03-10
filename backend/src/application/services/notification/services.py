from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.repositories.notification.crud import NotificationRepository
from domain.dtos.notification.dtos import NotificationCreate, NotificationResponse


class NotificationService:
    """Service class for handling notification operations."""

    def __init__(self, notification_repository: NotificationRepository):
        self.repository = notification_repository

    def create(
        self, db: Session, notification_create: NotificationCreate
    ) -> NotificationResponse:
        """
        Create a new notification.

        Args:
            db: Database session
            notification_create: Notification creation data transfer object

        Returns:
            The created Notification record

        Raises:
            HTTPException: If there's an error creating the notification
        """
        try:
            return self.repository.create(db, notification_create)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating notification: {str(e)}"
            )

    def get_latest_unread(
        self, db: Session, limit: int = 20
    ) -> List[NotificationResponse]:
        """
        Get the latest unread notifications.

        Args:
            db: Database session
            limit: Maximum number of records to return (default 20)

        Returns:
            List of unread Notification records

        Raises:
            HTTPException: If there's an error retrieving the notifications
        """
        try:
            notifications = self.repository.get_latest_unread(db, limit)
            if not notifications:
                raise HTTPException(
                    status_code=404, detail="No unread notifications found"
                )
            return notifications
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving unread notifications: {str(e)}",
            )

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
            List of Notification records

        Raises:
            HTTPException: If there's an error retrieving the notifications
        """
        try:
            notifications = self.repository.get_paginated(db, skip, limit)
            if not notifications:
                raise HTTPException(status_code=404, detail="No notifications found")
            return notifications
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving notifications: {str(e)}"
            )

    def update_read_status(
        self, db: Session, notification_id: int, is_read: bool = True
    ) -> NotificationResponse:
        """
        Update the read status of a notification.

        Args:
            db: Database session
            notification_id: The ID of the notification
            is_read: The new read status (default True)

        Returns:
            Updated Notification record

        Raises:
            HTTPException: If the notification is not found or if there's an error updating it
        """
        try:
            notification = self.repository.update_read_status(
                db, notification_id, is_read
            )
            if not notification:
                raise HTTPException(
                    status_code=404,
                    detail=f"Notification with id {notification_id} not found",
                )
            return notification
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error updating notification read status: {str(e)}",
            )

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
            List of Notification records for the specified MAC address

        Raises:
            HTTPException: If no notifications are found for the MAC address or if there's an error retrieving them
        """
        try:
            notifications = self.repository.get_by_mac_address(
                db, mac_address, skip, limit
            )
            if not notifications:
                raise HTTPException(
                    status_code=404,
                    detail=f"No notifications found for device with MAC address {mac_address}",
                )
            return notifications
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving notifications: {str(e)}"
            )
