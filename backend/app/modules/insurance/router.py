"""
MediCore Nexus - Insurance Management & Claims Adjudication
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.events import event_bus, EVENT_INSURANCE_CLAIM_SUBMITTED

class InsuranceClaimBase(BaseModel):
    patient_id: str
    patient_name: str
    insurance_provider: str
    policy_number: str
    group_number: str
    claim_type: str = "Outpatient & Pharmacy"
    billed_amount: float
    deductible_amount: float = 20.00
    copay_amount: float = 15.00
    diagnosis_codes: List[str]
    treatment_summary: str

class InsuranceClaimCreate(InsuranceClaimBase):
    pass

class InsuranceClaimResponse(InsuranceClaimBase):
    id: str
    claim_number: str
    status: str  # Submitted, Under Review, Pre-Authorized, Approved, Settled, Rejected
    approved_amount: float
    adjudication_notes: Optional[str] = None
    submitted_at: datetime
    settled_at: Optional[datetime] = None

CLAIMS_STORE: Dict[str, Dict] = {
    "clm-001": {
        "id": "clm-001",
        "claim_number": "CLM-2026-BCBS-88901",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "insurance_provider": "Blue Cross Blue Shield",
        "policy_number": "POL-BCBS-889104",
        "group_number": "GRP-TECH-7701",
        "claim_type": "Outpatient & Pharmacy",
        "billed_amount": 295.00,
        "deductible_amount": 0.00,
        "copay_amount": 35.00,
        "diagnosis_codes": ["I10", "E11.9", "E78.0"],
        "treatment_summary": "Comprehensive Cardiology Follow-up and Lipid Bloodwork.",
        "status": "Approved",
        "approved_amount": 260.00,
        "adjudication_notes": "Tier 1 preferred specialist visit. Full in-network coverage applied.",
        "submitted_at": datetime.now(timezone.utc) - timedelta(days=2),
        "settled_at": datetime.now(timezone.utc) - timedelta(days=1),
    }
}

router = APIRouter(prefix="/insurance", tags=["Insurance & Claims Adjudication"])

@router.get("/claims", response_model=List[InsuranceClaimResponse])
async def list_claims(patient_id: Optional[str] = None, status_filter: Optional[str] = None):
    res = list(CLAIMS_STORE.values())
    if patient_id:
        res = [c for c in res if c["patient_id"] == patient_id]
    if status_filter:
        res = [c for c in res if c["status"].lower() == status_filter.lower()]
    return res

@router.post("/claims", response_model=InsuranceClaimResponse, status_code=status.HTTP_201_CREATED)
async def submit_insurance_claim(claim_in: InsuranceClaimCreate):
    cid = f"clm-{uuid.uuid4().hex[:6]}"
    cnum = f"CLM-2026-{uuid.uuid4().hex[:6].upper()}"
    approved_amt = max(0.0, claim_in.billed_amount - claim_in.copay_amount - claim_in.deductible_amount)
    
    cdict = {
        "id": cid,
        "claim_number": cnum,
        "status": "Under Review",
        "approved_amount": approved_amt,
        "adjudication_notes": "Automated pre-adjudication eligible. Pending final insurer clearance.",
        **claim_in.dict(),
        "submitted_at": datetime.now(timezone.utc),
        "settled_at": None,
    }
    CLAIMS_STORE[cid] = cdict
    await event_bus.publish(EVENT_INSURANCE_CLAIM_SUBMITTED, cdict)
    return InsuranceClaimResponse(**cdict)
