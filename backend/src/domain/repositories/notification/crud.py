from typing import List, Optional, TypedDict
from sqlalchemy.orm import Session
from sqlalchemy import desc

from domain.models.notification import Notification

class CreateNotificationParams(TypedDict):
    """Parameters for creating a notification."""
    notification_type: str
    title: str
    description: Optional[str]

class PaginationParams(TypedDict):
    """Parameters for pagination."""
    skip: int
    limit: int

class NotificationRepository:
    """Repository for handling Notification CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, params: CreateNotificationParams) -> Notification:
        """
        Create a new notification.
        
        Args:
            params (CreateNotificationParams): Parameters for creating notification
                notification_type (str): Type of the notification
                title (str): Title of the notification
                description (Optional[str]): Description of the notification
            
        Returns:
            Notification: Created notification instance
        """
        notification = Notification(
            notification_type=params['notification_type'],
            title=params['title'],
            description=params.get('description'),
            is_read=False
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_paginated_list(self, params: PaginationParams) -> List[Notification]:
        """
        Get paginated list of notifications sorted by created_at in descending order.
        
        Args:
            params (PaginationParams): Pagination parameters
                skip (int): Number of records to skip (offset)
                limit (int): Maximum number of records to return
            
        Returns:
            List[Notification]: List of notifications
        """
        return self.db.query(Notification)\
            .order_by(desc(Notification.created_at))\
            .offset(params['skip'])\
            .limit(params['limit'])\
            .all()

    def update_read_status(self, notification_id: int) -> Optional[Notification]:
        """
        Update the read status of a notification to True.
        
        Args:
            notification_id (int): ID of the notification to update
            
        Returns:
            Optional[Notification]: Updated notification instance or None if not found
        """
        notification = self.db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            setattr(notification, 'is_read', True)
            self.db.commit()
            self.db.refresh(notification)
        return notification
