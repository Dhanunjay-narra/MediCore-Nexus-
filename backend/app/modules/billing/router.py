"""
MediCore Nexus - Billing & Revenue Management
Unified ledger across consultations, pharmacy dispensing, lab orders, and hospital stay
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

class InvoiceItem(BaseModel):
    service_type: str  # Consultation, Pharmacy, Laboratory, Room Charge, Procedure
    description: str
    quantity: int = 1
    unit_price: float
    discount: float = 0.0
    tax: float = 0.0
    net_total: float

class InvoiceBase(BaseModel):
    patient_id: str
    patient_name: str
    hospital_id: str = "hosp-001"
    insurance_claim_id: Optional[str] = None
    insurance_coverage_amount: float = 0.0
    patient_copay_amount: float = 0.0
    items: List[InvoiceItem]

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceResponse(InvoiceBase):
    id: str
    invoice_number: str
    subtotal: float
    total_tax: float
    total_discount: float
    gross_total: float
    balance_due: float
    payment_status: str  # Pending, Partially Paid, Paid, Void, Refunded
    created_at: datetime
    paid_at: Optional[datetime] = None

INVOICES_STORE: Dict[str, Dict] = {
    "inv-001": {
        "id": "inv-001",
        "invoice_number": "INV-2026-003891",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "hospital_id": "hosp-001",
        "insurance_claim_id": "clm-001",
        "insurance_coverage_amount": 260.00,
        "patient_copay_amount": 35.00,
        "subtotal": 295.00,
        "total_tax": 0.00,
        "total_discount": 0.00,
        "gross_total": 295.00,
        "balance_due": 0.00,
        "payment_status": "Paid",
        "created_at": datetime.now(timezone.utc) - timedelta(days=2),
        "paid_at": datetime.now(timezone.utc) - timedelta(days=2),
        "items": [
            {
                "service_type": "Consultation",
                "description": "Comprehensive Cardiac Consultation with Dr. Sarah Chen",
                "quantity": 1,
                "unit_price": 220.00,
                "discount": 0.0,
                "tax": 0.0,
                "net_total": 220.00,
            },
            {
                "service_type": "Laboratory",
                "description": "Lipid Panel & Metabolic Test Panel",
                "quantity": 1,
                "unit_price": 75.00,
                "discount": 0.0,
                "tax": 0.0,
                "net_total": 75.00,
            }
        ]
    }
}

router = APIRouter(prefix="/billing", tags=["Billing & Revenue Management"])

@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(patient_id: Optional[str] = None, status_filter: Optional[str] = None):
    res = list(INVOICES_STORE.values())
    if patient_id:
        res = [i for i in res if i["patient_id"] == patient_id]
    if status_filter:
        res = [i for i in res if i["payment_status"].lower() == status_filter.lower()]
    return res

@router.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: str):
    if invoice_id not in INVOICES_STORE:
        raise HTTPException(status_code=404, detail="Invoice record not found")
    return INVOICES_STORE[invoice_id]

@router.post("/invoices", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(inv_in: InvoiceCreate):
    iid = f"inv-{uuid.uuid4().hex[:6]}"
    inum = f"INV-2026-{uuid.uuid4().hex[:6].upper()}"
    
    subtot = sum(i.quantity * i.unit_price for i in inv_in.items)
    tot_tax = sum(i.tax for i in inv_in.items)
    tot_disc = sum(i.discount for i in inv_in.items)
    gross = subtot + tot_tax - tot_disc
    balance = gross - inv_in.insurance_coverage_amount
    
    idict = {
        "id": iid,
        "invoice_number": inum,
        "subtotal": subtot,
        "total_tax": tot_tax,
        "total_discount": tot_disc,
        "gross_total": gross,
        "balance_due": max(0.0, balance),
        "payment_status": "Pending" if balance > 0 else "Paid",
        **inv_in.dict(),
        "created_at": datetime.now(timezone.utc),
        "paid_at": None,
    }
    INVOICES_STORE[iid] = idict
    return InvoiceResponse(**idict)
