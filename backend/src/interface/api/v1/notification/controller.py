from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session

from domain.dtos.notification.dtos import NotificationCreate, NotificationResponse
from application.services.notification.services import NotificationService
from domain.repositories.notification.crud import NotificationRepository
from infrastructure.database.base import get_db
from infrastructure.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def get_notification_service() -> NotificationService:
    """
    Dependency provider for NotificationService.
    
    Returns:
        NotificationService: An instance of the notification service
    """
    return NotificationService(
        notification_repository=NotificationRepository()
    )

@router.post(
    "",
    response_model=NotificationResponse,
    summary="Create new notification",
    description="Creates a new notification for a device",
    status_code=201,
    responses={
        201: {"description": "Notification created successfully"},
        422: {"description": "Validation Error - Invalid data format"},
        500: {"description": "Internal server error"}
    }
)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> NotificationResponse:
    """
    Creates a new notification.
    
    Args:
        notification: Notification data transfer object containing:
            - device_id: The MAC address of the device (required)
            - type: Type of notification (required)
            - title: Title of the notification (required)
            - description: Optional description
        db: Database session
        notification_service: Service that handles notification operations
    
    Returns:
        NotificationResponse: The created notification data including creation timestamp
        
    Raises:
        HTTPException: 422 if data format is invalid
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Creating new notification for device: {notification.device_id}")
    response = notification_service.create(db, notification)
    logger.info(f"Notification created successfully: {response}")
    return response

@router.get(
    "/unread",
    response_model=List[NotificationResponse],
    summary="Get latest unread notifications",
    description="Retrieves the latest unread notifications"
)
async def get_latest_unread_notifications(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of notifications to return"),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> List[NotificationResponse]:
    """
    Retrieves the latest unread notifications.
    
    Args:
        limit: Maximum number of notifications to return
        db: Database session
        notification_service: Service that handles notification operations
    
    Returns:
        List[NotificationResponse]: List of unread notifications
        
    Raises:
        HTTPException: 404 if no unread notifications found
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Retrieving latest {limit} unread notifications")
    response = notification_service.get_latest_unread(db, limit)
    logger.info(f"Retrieved {len(response)} unread notifications successfully")
    return response

@router.get(
    "",
    response_model=List[NotificationResponse],
    summary="Get paginated notifications",
    description="Retrieves a paginated list of notifications"
)
async def get_notifications(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> List[NotificationResponse]:
    """
    Retrieves a paginated list of notifications.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        notification_service: Service that handles notification operations
    
    Returns:
        List[NotificationResponse]: List of notifications
        
    Raises:
        HTTPException: 404 if no notifications found
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Retrieving notifications with pagination: skip={skip}, limit={limit}")
    response = notification_service.get_paginated(db, skip, limit)
    logger.info(f"Retrieved {len(response)} notifications successfully")
    return response

@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Update notification read status",
    description="Updates the read status of a specific notification"
)
async def update_notification_read_status(
    notification_id: int,
    is_read: bool = Query(True, description="The new read status to set"),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> NotificationResponse:
    """
    Updates the read status of a specific notification.
    
    Args:
        notification_id: The ID of the notification
        is_read: The new read status to set (default: True)
        db: Database session
        notification_service: Service that handles notification operations
    
    Returns:
        NotificationResponse: The updated notification data
        
    Raises:
        HTTPException: 404 if notification not found
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Updating read status to {is_read} for notification ID: {notification_id}")
    response = notification_service.update_read_status(db, notification_id, is_read)
    logger.info(f"Notification read status updated successfully: {response}")
    return response

@router.get(
    "/device/{mac_address}",
    response_model=List[NotificationResponse],
    summary="Get notifications by device",
    description="Retrieves notifications for a specific device"
)
async def get_device_notifications(
    mac_address: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    notification_service: NotificationService = Depends(get_notification_service)
) -> List[NotificationResponse]:
    """
    Retrieves notifications for a specific device.
    
    Args:
        mac_address: The MAC address of the device
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (for pagination)
        db: Database session
        notification_service: Service that handles notification operations
    
    Returns:
        List[NotificationResponse]: List of notifications for the device
        
    Raises:
        HTTPException: 404 if no notifications found for the device
        HTTPException: 500 if there's a server error
    """
    logger.info(f"Retrieving notifications for device {mac_address} with pagination: skip={skip}, limit={limit}")
    response = notification_service.get_by_mac_address(db, mac_address, skip, limit)
    logger.info(f"Retrieved {len(response)} notifications successfully for device {mac_address}")
    return response
