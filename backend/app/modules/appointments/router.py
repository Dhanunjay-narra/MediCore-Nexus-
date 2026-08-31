"""
MediCore Nexus - Appointment & Queue Management
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.events import event_bus, EVENT_APPOINTMENT_SCHEDULED, EVENT_APPOINTMENT_CHECKED_IN

class AppointmentBase(BaseModel):
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    department_id: str
    appointment_type: str = "In-Person Consultation"  # In-Person Consultation, Telemedicine Video, Follow-up, STAT
    scheduled_datetime: str
    duration_minutes: int = 30
    reason_for_visit: str
    token_number: int = 1
    priority: str = "Normal"  # Routine, Urgent, Emergency

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: str
    status: str  # Scheduled, Confirmed, Checked-In, Waiting, In-Consultation, Completed, Cancelled, No-Show
    created_at: datetime
    checked_in_at: Optional[datetime] = None

APPOINTMENTS_STORE: Dict[str, Dict] = {
    "apt-001": {
        "id": "apt-001",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "department_id": "dept-cardio",
        "appointment_type": "In-Person Consultation",
        "scheduled_datetime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "duration_minutes": 30,
        "reason_for_visit": "Quarterly cardiovascular evaluation and blood pressure review",
        "token_number": 101,
        "priority": "Normal",
        "status": "Checked-In",
        "created_at": datetime.now(timezone.utc) - timedelta(days=2),
        "checked_in_at": datetime.now(timezone.utc) - timedelta(minutes=10),
    },
    "apt-002": {
        "id": "apt-002",
        "patient_id": "pat-002",
        "patient_name": "Michael Chang",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "department_id": "dept-cardio",
        "appointment_type": "Telemedicine Video",
        "scheduled_datetime": (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(),
        "duration_minutes": 20,
        "reason_for_visit": "Asthma medication titration and exercise tolerance assessment",
        "token_number": 102,
        "priority": "Normal",
        "status": "Confirmed",
        "created_at": datetime.now(timezone.utc) - timedelta(days=1),
        "checked_in_at": None,
    },
    "apt-003": {
        "id": "apt-003",
        "patient_id": "pat-003",
        "patient_name": "Sophia Martinez",
        "doctor_id": "doc-003",
        "doctor_name": "Dr. Emily Taylor, MD",
        "department_id": "dept-neuro",
        "appointment_type": "In-Person Consultation",
        "scheduled_datetime": (datetime.now(timezone.utc) + timedelta(hours=4, minutes=30)).isoformat(),
        "duration_minutes": 45,
        "reason_for_visit": "Refractory migraine aura consultation and prophylactic review",
        "token_number": 201,
        "priority": "Urgent",
        "status": "Scheduled",
        "created_at": datetime.now(timezone.utc) - timedelta(hours=5),
        "checked_in_at": None,
    }
}

router = APIRouter(prefix="/appointments", tags=["Appointment & Queue Management"])

@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    doctor_id: Optional[str] = None,
    patient_id: Optional[str] = None,
    status_filter: Optional[str] = None
):
    res = list(APPOINTMENTS_STORE.values())
    if doctor_id:
        res = [a for a in res if a["doctor_id"] == doctor_id]
    if patient_id:
        res = [a for a in res if a["patient_id"] == patient_id]
    if status_filter:
        res = [a for a in res if a["status"].lower() == status_filter.lower()]
    return res

@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(apt_in: AppointmentCreate):
    aid = f"apt-{uuid.uuid4().hex[:6]}"
    adict = {
        "id": aid,
        **apt_in.dict(),
        "status": "Scheduled",
        "created_at": datetime.now(timezone.utc),
        "checked_in_at": None,
    }
    APPOINTMENTS_STORE[aid] = adict
    await event_bus.publish(EVENT_APPOINTMENT_SCHEDULED, adict)
    return AppointmentResponse(**adict)

@router.put("/{appointment_id}/check-in", response_model=AppointmentResponse)
async def check_in_appointment(appointment_id: str):
    if appointment_id not in APPOINTMENTS_STORE:
        raise HTTPException(status_code=404, detail="Appointment not found")
    apt = APPOINTMENTS_STORE[appointment_id]
    apt["status"] = "Checked-In"
    apt["checked_in_at"] = datetime.now(timezone.utc)
    await event_bus.publish(EVENT_APPOINTMENT_CHECKED_IN, apt)
    return AppointmentResponse(**apt)

@router.put("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status(appointment_id: str, new_status: str):
    if appointment_id not in APPOINTMENTS_STORE:
        raise HTTPException(status_code=404, detail="Appointment not found")
    apt = APPOINTMENTS_STORE[appointment_id]
    apt["status"] = new_status
    return AppointmentResponse(**apt)
