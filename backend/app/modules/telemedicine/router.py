"""
MediCore Nexus - Telemedicine & Virtual Consultations
Simulated WebRTC sessions, real-time consultation notes, and video rooms
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

class TelemedicineSessionBase(BaseModel):
    appointment_id: str
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    scheduled_start: str
    room_token: str
    is_video_enabled: bool = True
    is_audio_enabled: bool = True
    clinical_notes: Optional[str] = None

class TelemedicineSessionResponse(TelemedicineSessionBase):
    id: str
    session_status: str  # Scheduled, Waiting, In-Call, Completed, Missed
    call_duration_seconds: int = 0
    created_at: datetime

TELEMEDICINE_SESSIONS: Dict[str, Dict] = {
    "tel-001": {
        "id": "tel-001",
        "appointment_id": "apt-002",
        "patient_id": "pat-002",
        "patient_name": "Michael Chang",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "scheduled_start": (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(),
        "room_token": "ROOM-WEBRTC-CHENG-CARDIO-88912",
        "is_video_enabled": True,
        "is_audio_enabled": True,
        "clinical_notes": "Remote review of peak flow readings and bronchodilator frequency.",
        "session_status": "Scheduled",
        "call_duration_seconds": 0,
        "created_at": datetime.now(timezone.utc) - timedelta(days=1),
    }
}

router = APIRouter(prefix="/telemedicine", tags=["Telemedicine & Virtual Care"])

@router.get("/sessions", response_model=List[TelemedicineSessionResponse])
async def list_telemedicine_sessions(doctor_id: Optional[str] = None, patient_id: Optional[str] = None):
    res = list(TELEMEDICINE_SESSIONS.values())
    if doctor_id:
        res = [t for t in res if t["doctor_id"] == doctor_id]
    if patient_id:
        res = [t for t in res if t["patient_id"] == patient_id]
    return res

@router.get("/sessions/{session_id}", response_model=TelemedicineSessionResponse)
async def get_telemedicine_session(session_id: str):
    if session_id not in TELEMEDICINE_SESSIONS:
        raise HTTPException(status_code=404, detail="Telemedicine session not found")
    return TELEMEDICINE_SESSIONS[session_id]

@router.put("/sessions/{session_id}/join")
async def join_session(session_id: str):
    if session_id not in TELEMEDICINE_SESSIONS:
        raise HTTPException(status_code=404, detail="Telemedicine session not found")
    sess = TELEMEDICINE_SESSIONS[session_id]
    sess["session_status"] = "In-Call"
    return {
        "session_id": session_id,
        "room_token": sess["room_token"],
        "status": "In-Call",
        "webrtc_ice_servers": [{"urls": "stun:stun.l.google.com:19302"}],
        "message": "Connected to secure HIPAA-compliant virtual room."
    }
