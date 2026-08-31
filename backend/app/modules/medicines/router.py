"""
MediCore Nexus - Pharmacy Product & Medicine Master Catalog
"""

import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query

class MedicineMasterBase(BaseModel):
    brand_name: str
    generic_name: str
    sku_code: str
    barcode: str
    dosage_form: str  # Tablet, Capsule, Syrup, Injection, Inhaler, Ointment, IV Infusion
    strength: str  # 500mg, 10mg/ml, etc.
    unit_of_measure: str  # Box, Bottle, Strip, Vial
    route_of_administration: str  # Oral, Intravenous, Subcutaneous, Inhalation, Topical
    manufacturer: str
    therapeutic_class: str
    is_prescription_required: bool = True
    is_controlled_substance: bool = False
    controlled_schedule: Optional[str] = None  # Schedule II, IV, None
    storage_condition: str = "Store below 25°C in a dry place"
    contraindications: List[str] = []
    standard_unit_price: float
    mrp: float

class MedicineMasterResponse(MedicineMasterBase):
    id: str
    is_active: bool

MEDICINES_CATALOG: Dict[str, Dict] = {
    "med-001": {
        "id": "med-001",
        "brand_name": "Lipitor",
        "generic_name": "Atorvastatin Calcium",
        "sku_code": "SKU-ATV-40MG",
        "barcode": "8901088231901",
        "dosage_form": "Tablet",
        "strength": "40 mg",
        "unit_of_measure": "Strip of 10 Tablets",
        "route_of_administration": "Oral",
        "manufacturer": "Pfizer Pharmaceuticals",
        "therapeutic_class": "HMG-CoA Reductase Inhibitor (Statin)",
        "is_prescription_required": True,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store at 20°C to 25°C (68°F to 77°F)",
        "contraindications": ["Active Liver Disease", "Pregnancy / Nursing", "Severe Renal Impairment"],
        "standard_unit_price": 14.50,
        "mrp": 18.00,
        "is_active": True,
    },
    "med-002": {
        "id": "med-002",
        "brand_name": "Glucophage XR",
        "generic_name": "Metformin Hydrochloride Extended-Release",
        "sku_code": "SKU-MET-500MG-XR",
        "barcode": "8901088231902",
        "dosage_form": "Extended-Release Tablet",
        "strength": "500 mg",
        "unit_of_measure": "Box of 60 Tablets",
        "route_of_administration": "Oral",
        "manufacturer": "Merck Healthcare",
        "therapeutic_class": "Biguanide Antidiabetic",
        "is_prescription_required": True,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store below 30°C. Protect from light and moisture.",
        "contraindications": ["Severe Renal Dysfunction (eGFR < 30)", "Acute Metabolic Acidosis / DKA"],
        "standard_unit_price": 9.20,
        "mrp": 12.50,
        "is_active": True,
    },
    "med-003": {
        "id": "med-003",
        "brand_name": "Amoxil",
        "generic_name": "Amoxicillin Trihydrate",
        "sku_code": "SKU-AMX-500MG",
        "barcode": "8901088231903",
        "dosage_form": "Capsule",
        "strength": "500 mg",
        "unit_of_measure": "Strip of 20 Capsules",
        "route_of_administration": "Oral",
        "manufacturer": "GlaxoSmithKline (GSK)",
        "therapeutic_class": "Beta-Lactam Penicillin Antibiotic",
        "is_prescription_required": True,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store at room temperature 15°C - 25°C",
        "contraindications": ["Known Penicillin Allergy", "Infectious Mononucleosis"],
        "standard_unit_price": 8.00,
        "mrp": 11.00,
        "is_active": True,
    },
    "med-004": {
        "id": "med-004",
        "brand_name": "Ventolin HFA",
        "generic_name": "Albuterol / Salbutamol Sulfate",
        "sku_code": "SKU-ALB-100MCG",
        "barcode": "8901088231904",
        "dosage_form": "Metered Dose Inhaler",
        "strength": "100 mcg/actuation",
        "unit_of_measure": "Canister (200 Puffs)",
        "route_of_administration": "Inhalation",
        "manufacturer": "GlaxoSmithKline (GSK)",
        "therapeutic_class": "Short-Acting Beta-2 Agonist (SABA) Bronchodilator",
        "is_prescription_required": True,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store upright between 15°C and 25°C. Do not puncture.",
        "contraindications": ["Hypersensitivity to Albuterol"],
        "standard_unit_price": 22.00,
        "mrp": 28.50,
        "is_active": True,
    },
    "med-005": {
        "id": "med-005",
        "brand_name": "Tylenol Extra Strength",
        "generic_name": "Acetaminophen / Paracetamol",
        "sku_code": "SKU-APAP-500MG",
        "barcode": "8901088231905",
        "dosage_form": "Caplet",
        "strength": "500 mg",
        "unit_of_measure": "Bottle of 100 Caplets",
        "route_of_administration": "Oral",
        "manufacturer": "Johnson & Johnson",
        "therapeutic_class": "Analgesic & Antipyretic (OTC)",
        "is_prescription_required": False,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store at 20°C to 25°C",
        "contraindications": ["Severe Hepatic Impairment", "Acute Liver Failure"],
        "standard_unit_price": 6.50,
        "mrp": 8.99,
        "is_active": True,
    },
    "med-006": {
        "id": "med-006",
        "brand_name": "Plavix",
        "generic_name": "Clopidogrel Bisulfate",
        "sku_code": "SKU-CLOP-75MG",
        "barcode": "8901088231906",
        "dosage_form": "Film-Coated Tablet",
        "strength": "75 mg",
        "unit_of_measure": "Box of 28 Tablets",
        "route_of_administration": "Oral",
        "manufacturer": "Sanofi",
        "therapeutic_class": "P2Y12 Platelet Inhibitor / Antiplatelet",
        "is_prescription_required": True,
        "is_controlled_substance": False,
        "controlled_schedule": None,
        "storage_condition": "Store below 25°C",
        "contraindications": ["Active Pathological Bleeding (e.g., Peptic Ulcer, Intracranial)", "Severe Hepatic Disease"],
        "standard_unit_price": 28.00,
        "mrp": 35.00,
        "is_active": True,
    },
}

router = APIRouter(prefix="/medicines", tags=["Pharmacy Product & Medicine Catalog"])

@router.get("", response_model=List[MedicineMasterResponse])
async def list_medicines(
    query: Optional[str] = Query(None, description="Search by brand name, generic name, barcode or SKU"),
    therapeutic_class: Optional[str] = None,
    rx_only: Optional[bool] = None,
):
    res = list(MEDICINES_CATALOG.values())
    if query:
        q = query.lower()
        res = [
            m for m in res
            if q in m["brand_name"].lower()
            or q in m["generic_name"].lower()
            or q in m["barcode"].lower()
            or q in m["sku_code"].lower()
        ]
    if therapeutic_class:
        t = therapeutic_class.lower()
        res = [m for m in res if t in m["therapeutic_class"].lower()]
    if rx_only is not None:
        res = [m for m in res if m["is_prescription_required"] == rx_only]
    return res

@router.get("/{medicine_id}", response_model=MedicineMasterResponse)
async def get_medicine(medicine_id: str):
    if medicine_id not in MEDICINES_CATALOG:
        raise HTTPException(status_code=404, detail="Medicine record not found in master catalog")
    return MEDICINES_CATALOG[medicine_id]
