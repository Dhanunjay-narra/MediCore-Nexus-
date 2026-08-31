"""
MediCore Nexus - Pharmacy Inventory Management
Batch tracking, Lot control, Expiry dates, Smart FEFO engine, and Low-stock alerts
"""

import uuid
from typing import List, Optional, Dict
from datetime import date, datetime, timezone, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query, status
from backend.app.modules.medicines.router import MEDICINES_CATALOG
from backend.app.events import event_bus, EVENT_LOW_STOCK_DETECTED, EVENT_STOCK_DEDUCTED

class InventoryBatchBase(BaseModel):
    medicine_id: str
    batch_number: str
    lot_number: str
    expiry_date: str  # YYYY-MM-DD
    manufacturing_date: str  # YYYY-MM-DD
    quantity_on_hand: int
    quantity_reserved: int = 0
    reorder_level: int = 50
    cost_per_unit: float
    selling_price_per_unit: float
    warehouse_name: str = "Central Hospital Pharmacy Depot"
    shelf_location: str = "Aisle 3 - Shelf B2"
    supplier_id: str = "sup-001"

class InventoryBatchResponse(InventoryBatchBase):
    id: str
    medicine_name: str
    days_to_expiry: int
    is_near_expiry: bool
    is_expired: bool
    is_low_stock: bool

INVENTORY_BATCHES: Dict[str, Dict] = {
    "bat-001": {
        "id": "bat-001",
        "medicine_id": "med-001",
        "medicine_name": "Lipitor (Atorvastatin 40mg)",
        "batch_number": "ATV-2026-B1",
        "lot_number": "LOT-8891-PF",
        "expiry_date": "2026-11-30",
        "manufacturing_date": "2025-05-15",
        "quantity_on_hand": 140,
        "quantity_reserved": 10,
        "reorder_level": 50,
        "cost_per_unit": 11.20,
        "selling_price_per_unit": 18.00,
        "warehouse_name": "Central Hospital Pharmacy Depot",
        "shelf_location": "Aisle 1 - Shelf A3",
        "supplier_id": "sup-001",
    },
    "bat-002": {
        "id": "bat-002",
        "medicine_id": "med-001",
        "medicine_name": "Lipitor (Atorvastatin 40mg)",
        "batch_number": "ATV-2027-B2",
        "lot_number": "LOT-9920-PF",
        "expiry_date": "2027-04-30",
        "manufacturing_date": "2025-10-10",
        "quantity_on_hand": 300,
        "quantity_reserved": 0,
        "reorder_level": 50,
        "cost_per_unit": 11.00,
        "selling_price_per_unit": 18.00,
        "warehouse_name": "Central Hospital Pharmacy Depot",
        "shelf_location": "Aisle 1 - Shelf A4",
        "supplier_id": "sup-001",
    },
    "bat-003": {
        "id": "bat-003",
        "medicine_id": "med-002",
        "medicine_name": "Glucophage XR (Metformin 500mg)",
        "batch_number": "MET-2026-M1",
        "lot_number": "LOT-4412-MK",
        "expiry_date": "2026-10-15",
        "manufacturing_date": "2025-04-01",
        "quantity_on_hand": 28,  # Below reorder level 50 -> Low Stock!
        "quantity_reserved": 5,
        "reorder_level": 50,
        "cost_per_unit": 7.50,
        "selling_price_per_unit": 12.50,
        "warehouse_name": "Central Hospital Pharmacy Depot",
        "shelf_location": "Aisle 2 - Shelf B1",
        "supplier_id": "sup-002",
    },
    "bat-004": {
        "id": "bat-004",
        "medicine_id": "med-003",
        "medicine_name": "Amoxil (Amoxicillin 500mg)",
        "batch_number": "AMX-2026-G1",
        "lot_number": "LOT-7731-GSK",
        "expiry_date": "2026-09-20",  # Near Expiry!
        "manufacturing_date": "2025-03-10",
        "quantity_on_hand": 85,
        "quantity_reserved": 0,
        "reorder_level": 40,
        "cost_per_unit": 6.80,
        "selling_price_per_unit": 11.00,
        "warehouse_name": "Emergency Ward Pharmacy",
        "shelf_location": "Aisle 3 - Shelf C1",
        "supplier_id": "sup-003",
    },
    "bat-005": {
        "id": "bat-005",
        "medicine_id": "med-004",
        "medicine_name": "Ventolin HFA (Albuterol Inhaler)",
        "batch_number": "ALB-2027-V1",
        "lot_number": "LOT-5519-GSK",
        "expiry_date": "2027-08-31",
        "manufacturing_date": "2025-08-01",
        "quantity_on_hand": 60,
        "quantity_reserved": 2,
        "reorder_level": 25,
        "cost_per_unit": 18.00,
        "selling_price_per_unit": 28.50,
        "warehouse_name": "Central Hospital Pharmacy Depot",
        "shelf_location": "Aisle 4 - Shelf D2",
        "supplier_id": "sup-003",
    },
    "bat-006": {
        "id": "bat-006",
        "medicine_id": "med-005",
        "medicine_name": "Tylenol Extra Strength (Acetaminophen 500mg)",
        "batch_number": "TYL-2027-T1",
        "lot_number": "LOT-1192-JJ",
        "expiry_date": "2027-12-31",
        "manufacturing_date": "2025-11-20",
        "quantity_on_hand": 210,
        "quantity_reserved": 0,
        "reorder_level": 50,
        "cost_per_unit": 4.50,
        "selling_price_per_unit": 8.99,
        "warehouse_name": "Retail OTC Pharmacy Counter",
        "shelf_location": "OTC Front Display Bay 2",
        "supplier_id": "sup-002",
    },
    "bat-007": {
        "id": "bat-007",
        "medicine_id": "med-006",
        "medicine_name": "Plavix (Clopidogrel 75mg)",
        "batch_number": "PLV-2026-P1",
        "lot_number": "LOT-3329-SNF",
        "expiry_date": "2026-12-15",
        "manufacturing_date": "2025-06-01",
        "quantity_on_hand": 45,
        "quantity_reserved": 5,
        "reorder_level": 40,
        "cost_per_unit": 22.50,
        "selling_price_per_unit": 35.00,
        "warehouse_name": "Central Hospital Pharmacy Depot",
        "shelf_location": "Aisle 1 - Shelf A2",
        "supplier_id": "sup-001",
    }
}

router = APIRouter(prefix="/inventory", tags=["Pharmacy Inventory Management"])

def enrich_batch(b: Dict) -> InventoryBatchResponse:
    today = date.today()
    exp = datetime.strptime(b["expiry_date"], "%Y-%m-%d").date()
    days_left = (exp - today).days
    return InventoryBatchResponse(
        **b,
        days_to_expiry=days_left,
        is_near_expiry=days_left <= 90 and days_left > 0,
        is_expired=days_left <= 0,
        is_low_stock=b["quantity_on_hand"] <= b["reorder_level"],
    )

@router.get("", response_model=List[InventoryBatchResponse])
async def list_inventory(
    medicine_id: Optional[str] = None,
    near_expiry_only: bool = False,
    low_stock_only: bool = False
):
    res = [enrich_batch(b) for b in INVENTORY_BATCHES.values()]
    if medicine_id:
        res = [b for b in res if b.medicine_id == medicine_id]
    if near_expiry_only:
        res = [b for b in res if b.is_near_expiry or b.is_expired]
    if low_stock_only:
        res = [b for b in res if b.is_low_stock]
    return res

@router.get("/fefo-recommendation/{medicine_id}", response_model=List[InventoryBatchResponse])
async def get_smart_fefo_batches(medicine_id: str, quantity_needed: int = 1):
    """
    Smart FEFO Engine (First-Expiry-First-Out)
    Sorts batches by earliest expiry date and positive available stock.
    """
    batches = [
        enrich_batch(b)
        for b in INVENTORY_BATCHES.values()
        if b["medicine_id"] == medicine_id and (b["quantity_on_hand"] - b["quantity_reserved"]) > 0
    ]
    # Sort strictly by earliest expiry date
    sorted_batches = sorted(batches, key=lambda x: x.expiry_date)
    return sorted_batches
