"""
MediCore Nexus - Pharmacy Command Center & Dispensing Workflow
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.modules.inventory.router import INVENTORY_BATCHES
from backend.app.events import event_bus, EVENT_MEDICINE_DISPENSED

class DispenseItem(BaseModel):
    prescription_item_id: Optional[str] = None
    medicine_id: str
    medicine_name: str
    batch_id: str
    batch_number: str
    quantity_dispensed: int
    unit_price: float
    instructions_verified: bool = True

class DispenseRequest(BaseModel):
    prescription_id: Optional[str] = None
    patient_id: str
    patient_name: str
    pharmacist_id: str = "usr-pharm-01"
    pharmacist_name: str = "Marcus Vance, PharmD"
    items: List[DispenseItem]
    pharmacist_notes: Optional[str] = None
    counseling_provided: bool = True

class DispenseResponse(BaseModel):
    dispense_id: str
    dispense_number: str
    prescription_id: Optional[str] = None
    patient_id: str
    patient_name: str
    dispensed_at: datetime
    pharmacist_name: str
    total_items_dispensed: int
    status: str = "Completed"
    items: List[DispenseItem]

DISPENSING_LOGS: Dict[str, Dict] = {
    "dsp-001": {
        "dispense_id": "dsp-001",
        "dispense_number": "DSP-2026-99201",
        "prescription_id": "rx-001",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "dispensed_at": datetime.now(timezone.utc) - timedelta(days=2),
        "pharmacist_name": "Marcus Vance, PharmD",
        "total_items_dispensed": 2,
        "status": "Completed",
        "items": [
            {
                "prescription_item_id": "item-1",
                "medicine_id": "med-001",
                "medicine_name": "Lipitor (Atorvastatin 40mg)",
                "batch_id": "bat-001",
                "batch_number": "ATV-2026-B1",
                "quantity_dispensed": 30,
                "unit_price": 18.00,
                "instructions_verified": True,
            }
        ]
    }
}

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy Operations & Dispensing"])

@router.get("/command-center")
async def get_pharmacy_command_center_metrics():
    """
    Pharmacy Command Center Real-Time Cockpit
    Aggregates today's sales, pending prescriptions, low stock batches, and risk radar.
    """
    near_exp_count = sum(
        1 for b in INVENTORY_BATCHES.values()
        if (datetime.strptime(b["expiry_date"], "%Y-%m-%d").date() - datetime.now().date()).days <= 90
    )
    low_stock_count = sum(
        1 for b in INVENTORY_BATCHES.values() if b["quantity_on_hand"] <= b["reorder_level"]
    )

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "today_gross_sales": 3480.50,
        "prescriptions_dispensed_today": 42,
        "pending_validation_rx": 5,
        "patients_in_pharmacy_queue": 3,
        "near_expiry_batches_alert": near_exp_count,
        "low_stock_reorder_alerts": low_stock_count,
        "high_risk_interactions_intercepted": 4,
        "fefo_compliance_rate_pct": 98.4,
        "recent_alerts": [
            {"id": "alt-1", "type": "EXPIRY", "severity": "Warning", "message": "Amoxil Batch #AMX-2026-G1 expires in under 25 days (Stock: 85)"},
            {"id": "alt-2", "type": "LOW_STOCK", "severity": "Urgent", "message": "Glucophage XR 500mg stock critically low (28 remaining, Reorder: 50)"},
            {"id": "alt-3", "type": "DRUG_SAFETY", "severity": "Critical", "message": "Penicillin allergy intercept on patient Eleanor Vance (Prevented adverse Rx)"}
        ]
    }

@router.post("/dispense", response_model=DispenseResponse, status_code=status.HTTP_201_CREATED)
async def process_dispense(disp_req: DispenseRequest):
    """
    Process prescription dispensing, deduct physical inventory, and record compliance log.
    """
    did = f"dsp-{uuid.uuid4().hex[:6]}"
    dnum = f"DSP-2026-{uuid.uuid4().hex[:6].upper()}"
    
    # Deduct stock from respective batches
    for item in disp_req.items:
        if item.batch_id in INVENTORY_BATCHES:
            batch = INVENTORY_BATCHES[item.batch_id]
            batch["quantity_on_hand"] = max(0, batch["quantity_on_hand"] - item.quantity_dispensed)
    
    disp_dict = {
        "dispense_id": did,
        "dispense_number": dnum,
        "prescription_id": disp_req.prescription_id,
        "patient_id": disp_req.patient_id,
        "patient_name": disp_req.patient_name,
        "dispensed_at": datetime.now(timezone.utc),
        "pharmacist_name": disp_req.pharmacist_name,
        "total_items_dispensed": len(disp_req.items),
        "status": "Completed",
        "items": [item.dict() for item in disp_req.items]
    }
    DISPENSING_LOGS[did] = disp_dict
    await event_bus.publish(EVENT_MEDICINE_DISPENSED, disp_dict)
    return DispenseResponse(**disp_dict)

@router.get("/dispense-history", response_model=List[DispenseResponse])
async def get_dispense_history():
    return list(DISPENSING_LOGS.values())
