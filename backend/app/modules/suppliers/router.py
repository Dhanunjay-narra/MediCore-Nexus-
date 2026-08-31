"""
MediCore Nexus - Supplier & Vendor Management
"""

import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, HTTPException

class SupplierBase(BaseModel):
    name: str
    contact_person: str
    email: EmailStr
    phone: str
    address: str
    city: str
    state: str
    tax_id: str
    payment_terms: str = "Net 30 Days"
    rating: float = 4.8
    category: str = "Pharmaceutical Wholesaler"

class SupplierResponse(SupplierBase):
    id: str
    is_active: bool

SUPPLIERS_STORE: Dict[str, Dict] = {
    "sup-001": {
        "id": "sup-001",
        "name": "AmerisourceBergen Healthcare Distribution",
        "contact_person": "Karen Sterling",
        "email": "karen.s@amerisource.example.com",
        "phone": "+1 (555) 882-9901",
        "address": "1300 Morris Drive",
        "city": "Chesterbrook",
        "state": "PA",
        "tax_id": "EIN-88391024",
        "payment_terms": "Net 30 Days",
        "rating": 4.9,
        "category": "Direct Pharmaceutical Distributor",
        "is_active": True,
    },
    "sup-002": {
        "id": "sup-002",
        "name": "McKesson Medical Supply Corp",
        "contact_person": "Robert Vance Jr.",
        "email": "robert.v@mckesson.example.com",
        "phone": "+1 (555) 773-1029",
        "address": "6555 State Hwy 161",
        "city": "Irving",
        "state": "TX",
        "tax_id": "EIN-99201948",
        "payment_terms": "Net 45 Days",
        "rating": 4.85,
        "category": "Global Drug & Device Wholesaler",
        "is_active": True,
    },
    "sup-003": {
        "id": "sup-003",
        "name": "Cardinal Health Pharma Logistics",
        "contact_person": "Lisa Huang",
        "email": "lisa.h@cardinal.example.com",
        "phone": "+1 (555) 349-8802",
        "address": "7000 Cardinal Place",
        "city": "Dublin",
        "state": "OH",
        "tax_id": "EIN-44910284",
        "payment_terms": "Net 30 Days",
        "rating": 4.75,
        "category": "Specialty & Controlled Substances Depot",
        "is_active": True,
    }
}

router = APIRouter(prefix="/suppliers", tags=["Supplier & Vendor Management"])

@router.get("", response_model=List[SupplierResponse])
async def list_suppliers():
    return list(SUPPLIERS_STORE.values())

@router.get("/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(supplier_id: str):
    if supplier_id not in SUPPLIERS_STORE:
        raise HTTPException(status_code=404, detail="Supplier record not found")
    return SUPPLIERS_STORE[supplier_id]
