"""
MediCore Nexus - Pharmacy & Hospital Staff Management
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

class StaffMember(BaseModel):
    id: str
    user_id: str
    full_name: str
    role_title: str
    department_id: str
    hospital_id: str
    shift_name: str  # Morning Shift (07:00-15:30), Evening Shift (15:00-23:30), Night STAT Shift (23:00-07:30)
    assigned_counter: Optional[str] = None
    duty_status: str  # On Duty, On Break, Off Duty, On Leave
    attendance_pct: float = 98.2

STAFF_ROSTER: Dict[str, Dict] = {
    "stf-001": {
        "id": "stf-001",
        "user_id": "usr-pharm-01",
        "full_name": "Marcus Vance, PharmD",
        "role_title": "Chief Clinical Pharmacist",
        "department_id": "dept-pharm",
        "hospital_id": "hosp-001",
        "shift_name": "Morning Shift (08:00 - 16:30)",
        "assigned_counter": "Dispensing Counter 1 (High Priority Rx)",
        "duty_status": "On Duty",
        "attendance_pct": 99.1,
    },
    "stf-002": {
        "id": "stf-002",
        "user_id": "usr-nurse-01",
        "full_name": "Elena Rodriguez, RN",
        "role_title": "Lead Triage Nurse",
        "department_id": "dept-er",
        "hospital_id": "hosp-001",
        "shift_name": "Day Triage Shift (07:00 - 19:30)",
        "assigned_counter": "ER Triage Bay 1",
        "duty_status": "On Duty",
        "attendance_pct": 98.4,
    },
    "stf-003": {
        "id": "stf-003",
        "user_id": "usr-lab-01",
        "full_name": "David Kim, MLS",
        "role_title": "Senior Clinical Laboratory Technologist",
        "department_id": "dept-lab",
        "hospital_id": "hosp-001",
        "shift_name": "Standard Lab Operations (08:30 - 17:00)",
        "assigned_counter": "Automated Chemistry Bench",
        "duty_status": "On Duty",
        "attendance_pct": 97.8,
    }
}

router = APIRouter(prefix="/staff", tags=["Pharmacy & Hospital Staff Management"])

@router.get("", response_model=List[StaffMember])
async def list_staff_roster():
    return list(STAFF_ROSTER.values())
