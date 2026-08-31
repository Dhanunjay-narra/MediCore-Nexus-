"""
MediCore Nexus - Laboratory Management
Test Catalog, Lab Orders, Sample Barcoding, Results Entry, and Critical Value Alerting
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.events import event_bus, EVENT_LAB_ORDER_CREATED, EVENT_LAB_RESULT_VERIFIED

class LabTestItem(BaseModel):
    test_code: str
    test_name: str
    parameter_name: str
    measured_value: Optional[str] = None
    unit: str
    reference_range_min: float
    reference_range_max: float
    is_abnormal: bool = False
    is_critical: bool = False
    flag: Optional[str] = None  # Normal, High, Low, Critical High, Critical Low

class LabOrderBase(BaseModel):
    patient_id: str
    patient_name: str
    doctor_id: str
    doctor_name: str
    order_type: str = "Routine"  # Routine, STAT, Pre-Op
    sample_type: str = "Venous Whole Blood"  # Blood, Urine, Sputum, CSF
    tests: List[LabTestItem]
    clinical_indication: str

class LabOrderCreate(LabOrderBase):
    pass

class LabOrderResponse(LabOrderBase):
    id: str
    order_number: str
    sample_barcode: str
    status: str  # Ordered, Sample Collected, Processing, Verified, Reported
    ordered_at: datetime
    reported_at: Optional[datetime] = None
    technician_name: Optional[str] = None

LAB_ORDERS: Dict[str, Dict] = {
    "lab-001": {
        "id": "lab-001",
        "order_number": "LAB-2026-009101",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "doctor_id": "doc-001",
        "doctor_name": "Dr. Sarah Chen, MD",
        "order_type": "Routine",
        "sample_type": "Venous Whole Blood & Serum",
        "sample_barcode": "BAR-LAB-99201",
        "clinical_indication": "Follow-up monitoring for statin therapy and type 2 diabetes.",
        "status": "Verified",
        "ordered_at": datetime.now(timezone.utc) - timedelta(days=4),
        "reported_at": datetime.now(timezone.utc) - timedelta(days=3),
        "technician_name": "David Kim, MLS",
        "tests": [
            {
                "test_code": "LIPID-LDL",
                "test_name": "Lipid Panel",
                "parameter_name": "LDL Cholesterol",
                "measured_value": "94",
                "unit": "mg/dL",
                "reference_range_min": 0,
                "reference_range_max": 100,
                "is_abnormal": False,
                "is_critical": False,
                "flag": "Normal",
            },
            {
                "test_code": "GLUC-A1C",
                "test_name": "Glycated Hemoglobin",
                "parameter_name": "Hemoglobin A1c",
                "measured_value": "6.8",
                "unit": "%",
                "reference_range_min": 4.0,
                "reference_range_max": 5.6,
                "is_abnormal": True,
                "is_critical": False,
                "flag": "High (Controlled Diabetic)",
            },
            {
                "test_code": "RENAL-GFR",
                "test_name": "Comprehensive Metabolic Panel",
                "parameter_name": "Estimated GFR (eGFR)",
                "measured_value": "92",
                "unit": "mL/min/1.73m²",
                "reference_range_min": 60,
                "reference_range_max": 120,
                "is_abnormal": False,
                "is_critical": False,
                "flag": "Normal",
            }
        ]
    }
}

router = APIRouter(prefix="/laboratory", tags=["Laboratory Management"])

@router.get("/orders", response_model=List[LabOrderResponse])
async def list_lab_orders(patient_id: Optional[str] = None, status_filter: Optional[str] = None):
    res = list(LAB_ORDERS.values())
    if patient_id:
        res = [l for l in res if l["patient_id"] == patient_id]
    if status_filter:
        res = [l for l in res if l["status"].lower() == status_filter.lower()]
    return res

@router.get("/orders/{order_id}", response_model=LabOrderResponse)
async def get_lab_order(order_id: str):
    if order_id not in LAB_ORDERS:
        raise HTTPException(status_code=404, detail="Lab order record not found")
    return LAB_ORDERS[order_id]

@router.post("/orders", response_model=LabOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_lab_order(order_in: LabOrderCreate):
    lid = f"lab-{uuid.uuid4().hex[:6]}"
    lnum = f"LAB-2026-{uuid.uuid4().hex[:6].upper()}"
    barcode = f"BAR-LAB-{uuid.uuid4().hex[:8].upper()}"
    
    ldict = {
        "id": lid,
        "order_number": lnum,
        "sample_barcode": barcode,
        "status": "Ordered",
        **order_in.dict(),
        "ordered_at": datetime.now(timezone.utc),
        "reported_at": None,
        "technician_name": None,
    }
    LAB_ORDERS[lid] = ldict
    await event_bus.publish(EVENT_LAB_ORDER_CREATED, ldict)
    return LabOrderResponse(**ldict)

@router.put("/orders/{order_id}/verify", response_model=LabOrderResponse)
async def verify_lab_results(order_id: str, technician_name: str = "David Kim, MLS"):
    if order_id not in LAB_ORDERS:
        raise HTTPException(status_code=404, detail="Lab order not found")
    order = LAB_ORDERS[order_id]
    order["status"] = "Verified"
    order["technician_name"] = technician_name
    order["reported_at"] = datetime.now(timezone.utc)
    await event_bus.publish(EVENT_LAB_RESULT_VERIFIED, order)
    return LabOrderResponse(**order)
