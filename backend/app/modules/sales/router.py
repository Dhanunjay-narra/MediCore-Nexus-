"""
MediCore Nexus - Pharmacy Sales & Point-of-Sale (POS) Engine
Fast barcode scanning, OTC/Prescription checkout, taxes, discounts, and payments
"""

import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.modules.inventory.router import INVENTORY_BATCHES
from backend.app.events import event_bus, EVENT_MEDICINE_SOLD

class CartItem(BaseModel):
    medicine_id: str
    medicine_name: str
    batch_id: str
    batch_number: str
    quantity: int
    unit_price: float
    discount_pct: float = 0.0
    tax_pct: float = 5.0
    total_line_amount: float

class CheckoutRequest(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    patient_id: Optional[str] = None
    prescription_id: Optional[str] = None
    cashier_id: str = "usr-pharm-01"
    payment_method: str = "Credit Card"  # Cash, Credit Card, Debit Card, UPI, Insurance Split
    subtotal: float
    tax_amount: float
    discount_amount: float = 0.0
    total_paid: float
    items: List[CartItem]

class SaleReceiptResponse(BaseModel):
    sale_id: str
    invoice_number: str
    transaction_date: datetime
    customer_name: str
    payment_method: str
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_paid: float
    items: List[CartItem]
    status: str = "Paid"

SALES_HISTORY: Dict[str, Dict] = {
    "sale-001": {
        "sale_id": "sale-001",
        "invoice_number": "INV-POS-2026-00491",
        "transaction_date": datetime.now(timezone.utc) - timedelta(hours=2),
        "customer_name": "Eleanor Vance",
        "payment_method": "Credit Card",
        "subtotal": 54.00,
        "tax_amount": 2.70,
        "discount_amount": 0.0,
        "total_paid": 56.70,
        "items": [
            {
                "medicine_id": "med-001",
                "medicine_name": "Lipitor (Atorvastatin 40mg)",
                "batch_id": "bat-001",
                "batch_number": "ATV-2026-B1",
                "quantity": 3,
                "unit_price": 18.00,
                "discount_pct": 0.0,
                "tax_pct": 5.0,
                "total_line_amount": 56.70,
            }
        ],
        "status": "Paid",
    }
}

router = APIRouter(prefix="/sales", tags=["Pharmacy Point-of-Sale (POS) & Sales"])

@router.post("/checkout", response_model=SaleReceiptResponse, status_code=status.HTTP_201_CREATED)
async def process_pos_checkout(req: CheckoutRequest):
    """
    Process retail/outpatient point-of-sale checkout, decrement physical batch stock,
    and issue a finalized receipt.
    """
    sid = f"sale-{uuid.uuid4().hex[:6]}"
    inv_num = f"INV-POS-2026-{uuid.uuid4().hex[:6].upper()}"
    
    # Decrement inventory stock for each purchased item
    for item in req.items:
        if item.batch_id in INVENTORY_BATCHES:
            batch = INVENTORY_BATCHES[item.batch_id]
            batch["quantity_on_hand"] = max(0, batch["quantity_on_hand"] - item.quantity)

    sale_dict = {
        "sale_id": sid,
        "invoice_number": inv_num,
        "transaction_date": datetime.now(timezone.utc),
        "customer_name": req.customer_name,
        "payment_method": req.payment_method,
        "subtotal": req.subtotal,
        "tax_amount": req.tax_amount,
        "discount_amount": req.discount_amount,
        "total_paid": req.total_paid,
        "items": [i.dict() for i in req.items],
        "status": "Paid"
    }
    SALES_HISTORY[sid] = sale_dict
    await event_bus.publish(EVENT_MEDICINE_SOLD, sale_dict)
    return SaleReceiptResponse(**sale_dict)

@router.get("/receipts", response_model=List[SaleReceiptResponse])
async def list_sales_receipts():
    return list(SALES_HISTORY.values())
