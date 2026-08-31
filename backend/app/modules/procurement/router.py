"""
MediCore Nexus - Procurement & Purchase Order Management
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

class POItem(BaseModel):
    medicine_id: str
    medicine_name: str
    quantity_ordered: int
    unit_cost: float
    total_cost: float

class PurchaseOrderBase(BaseModel):
    supplier_id: str
    supplier_name: str
    expected_delivery_date: str
    destination_warehouse: str = "Central Hospital Pharmacy Depot"
    payment_terms: str = "Net 30"
    items: List[POItem]
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    pass

class PurchaseOrderResponse(PurchaseOrderBase):
    id: str
    po_number: str
    total_amount: float
    status: str  # Draft, Submitted, Approved, Shipped, Received, Cancelled
    created_at: datetime
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None

PURCHASE_ORDERS: Dict[str, Dict] = {
    "po-001": {
        "id": "po-001",
        "po_number": "PO-2026-00891",
        "supplier_id": "sup-002",
        "supplier_name": "McKesson Medical Supply Corp",
        "expected_delivery_date": "2026-09-05",
        "destination_warehouse": "Central Hospital Pharmacy Depot",
        "payment_terms": "Net 45",
        "items": [
            {
                "medicine_id": "med-002",
                "medicine_name": "Glucophage XR (Metformin 500mg)",
                "quantity_ordered": 200,
                "unit_cost": 7.50,
                "total_cost": 1500.00,
            }
        ],
        "notes": "Emergency restock due to inventory falling below threshold.",
        "total_amount": 1500.00,
        "status": "Approved",
        "created_at": datetime.now(timezone.utc) - timedelta(days=1),
        "approved_by": "Dr. Alexander Wright, MD",
        "approved_at": datetime.now(timezone.utc) - timedelta(hours=18),
    }
}

router = APIRouter(prefix="/procurement", tags=["Procurement & Purchase Orders"])

@router.get("/purchase-orders", response_model=List[PurchaseOrderResponse])
async def list_purchase_orders(status_filter: Optional[str] = None):
    res = list(PURCHASE_ORDERS.values())
    if status_filter:
        res = [p for p in res if p["status"].lower() == status_filter.lower()]
    return res

@router.post("/purchase-orders", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(po_in: PurchaseOrderCreate):
    poid = f"po-{uuid.uuid4().hex[:6]}"
    po_num = f"PO-2026-{uuid.uuid4().hex[:6].upper()}"
    tot = sum(item.total_cost for item in po_in.items)
    
    po_dict = {
        "id": poid,
        "po_number": po_num,
        "total_amount": tot,
        "status": "Submitted",
        **po_in.dict(),
        "created_at": datetime.now(timezone.utc),
        "approved_by": None,
        "approved_at": None,
    }
    PURCHASE_ORDERS[poid] = po_dict
    return PurchaseOrderResponse(**po_dict)
