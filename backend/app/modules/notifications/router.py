"""
MediCore Nexus - Central Notifications & Multi-Channel Communication
Email, SMS, Push, and WhatsApp Integrations
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

class NotificationItem(BaseModel):
    id: str
    recipient_user_id: str
    recipient_name: str
    channel: str  # In-App, SMS, Email, WhatsApp, Push
    category: str  # Appointment, Prescription, Lab Result, Inventory Alert, Clinical Risk
    title: str
    message: str
    is_read: bool = False
    sent_at: datetime

NOTIFICATIONS_STORE: List[Dict] = [
    {
        "id": "notif-001",
        "recipient_user_id": "usr-pat-01",
        "recipient_name": "Eleanor Vance",
        "channel": "SMS",
        "category": "Prescription",
        "title": "Prescription Ready for Pickup",
        "message": "Your prescription RX-2026-889101 (Lipitor 40mg, Glucophage XR) has been dispensed and is ready at Central Hospital Pharmacy Counter 1.",
        "is_read": False,
        "sent_at": datetime.now(timezone.utc) - timedelta(hours=1),
    },
    {
        "id": "notif-002",
        "recipient_user_id": "usr-pharm-01",
        "recipient_name": "Marcus Vance, PharmD",
        "channel": "In-App",
        "category": "Inventory Alert",
        "title": "Low Stock Alert: Metformin 500mg ER",
        "message": "Glucophage XR 500mg inventory is at 28 units (Reorder threshold: 50). Purchase Order #PO-2026-00891 is currently pending approval.",
        "is_read": False,
        "sent_at": datetime.now(timezone.utc) - timedelta(hours=3),
    },
    {
        "id": "notif-003",
        "recipient_user_id": "usr-doc-01",
        "recipient_name": "Dr. Sarah Chen, MD",
        "channel": "Push",
        "category": "Appointment",
        "title": "Patient Checked In",
        "message": "Patient Eleanor Vance has checked in for her 10:30 AM follow-up consultation in Suite 304.",
        "is_read": True,
        "sent_at": datetime.now(timezone.utc) - timedelta(minutes=15),
    }
]

router = APIRouter(prefix="/notifications", tags=["Notifications & Communications"])

@router.get("", response_model=List[NotificationItem])
async def list_notifications(user_id: Optional[str] = None):
    if user_id:
        return [n for n in NOTIFICATIONS_STORE if n["recipient_user_id"] == user_id]
    return NOTIFICATIONS_STORE

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    for n in NOTIFICATIONS_STORE:
        if n["id"] == notification_id:
            n["is_read"] = True
            return {"status": "success", "message": "Notification marked as read"}
    raise HTTPException(status_code=404, detail="Notification not found")
