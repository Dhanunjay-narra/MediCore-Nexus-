"""
MediCore Nexus - Drug Safety & Clinical Pharmacy Engine
Rule-based drug-drug interaction matrix, allergy checker, duplicate therapy, and Risk Radar
"""

import uuid
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status
from backend.app.modules.patients.router import PATIENTS_STORE
from backend.app.modules.medicines.router import MEDICINES_CATALOG

class SafetyCheckRequest(BaseModel):
    patient_id: str
    medicine_ids: List[str]
    current_condition_codes: List[str] = []

class DrugInteractionAlert(BaseModel):
    drug_a: str
    drug_b: str
    severity: str  # Critical, High, Moderate, Minor
    mechanism: str
    clinical_recommendation: str

class AllergyAlert(BaseModel):
    medicine_name: str
    allergen_matched: str
    severity: str = "Critical"
    clinical_recommendation: str

class SafetyCheckResult(BaseModel):
    patient_id: str
    overall_risk_level: str  # Normal, Medium, High, Critical
    risk_score_100: int
    is_safe_to_dispense: bool
    interaction_alerts: List[DrugInteractionAlert] = []
    allergy_alerts: List[AllergyAlert] = []
    contraindication_alerts: List[str] = []
    duplicate_therapy_alerts: List[str] = []
    special_population_warnings: List[str] = []

# Known Drug-Drug Interactions Knowledge Base
DRUG_INTERACTIONS_MATRIX = [
    {
        "drugs": {"med-001", "med-006"},  # Atorvastatin + Clopidogrel
        "severity": "Moderate",
        "mechanism": "Atorvastatin (CYP3A4 substrate/inhibitor) may slightly modulate Clopidogrel active metabolite formation. Monitor lipid and antiplatelet efficacy.",
        "recommendation": "Safe with monitoring. Alternatively, consider Rosuvastatin or Pravastatin which are not metabolized by CYP3A4.",
    },
    {
        "drugs": {"med-001", "med-003"},  # Atorvastatin + Amoxicillin
        "severity": "Minor",
        "mechanism": "No significant pharmacokinetic antagonism.",
        "recommendation": "Co-administration acceptable. Standard dosing applies.",
    },
    {
        "drugs": {"med-002", "med-006"},  # Metformin + Clopidogrel
        "severity": "Minor",
        "mechanism": "No documented drug-drug interaction.",
        "recommendation": "Safe to dispense concurrently.",
    }
]

router = APIRouter(prefix="/drug-safety", tags=["Drug Safety & Clinical Pharmacy"])

@router.post("/check", response_model=SafetyCheckResult)
async def check_medication_safety(req: SafetyCheckRequest):
    """
    Perform deep clinical safety check against patient allergies, medical history,
    and multi-drug interaction matrix.
    """
    patient = PATIENTS_STORE.get(req.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    allergy_alerts: List[AllergyAlert] = []
    interaction_alerts: List[DrugInteractionAlert] = []
    contraindication_alerts: List[str] = []
    duplicate_therapy_alerts: List[str] = []
    special_warnings: List[str] = []

    # 1. Check Allergies
    patient_allergies = [a.lower() for a in patient.get("allergies", [])]
    
    meds = [MEDICINES_CATALOG.get(mid) for mid in req.medicine_ids if mid in MEDICINES_CATALOG]
    
    for med in meds:
        mname = med["brand_name"].lower()
        gname = med["generic_name"].lower()
        tclass = med["therapeutic_class"].lower()

        # Penicillin / Beta-lactam allergy cross-reaction
        if any(alg in "penicillin" or alg in "amoxicillin" for alg in patient_allergies):
            if "penicillin" in tclass or "amoxicillin" in gname:
                allergy_alerts.append(AllergyAlert(
                    medicine_name=med["brand_name"],
                    allergen_matched="Penicillin / Beta-Lactam",
                    severity="Critical",
                    clinical_recommendation="DO NOT DISPENSE. Patient has documented Penicillin allergy. Risk of anaphylaxis. Substitute with Macrolide or Cephalosporin if tolerated."
                ))
        
        # Aspirin / NSAID allergy check
        if any(alg in "aspirin" or alg in "nsaid" or alg in "ibuprofen" for alg in patient_allergies):
            if "aspirin" in gname or "nsaid" in tclass:
                allergy_alerts.append(AllergyAlert(
                    medicine_name=med["brand_name"],
                    allergen_matched="Aspirin / NSAIDs",
                    severity="Critical",
                    clinical_recommendation="Patient has documented AERD / NSAID hypersensitivity. Avoid NSAIDs."
                ))

        # Check Chronic Contraindications
        for contra in med.get("contraindications", []):
            for condition in patient.get("chronic_conditions", []):
                if "renal" in contra.lower() and "renal" in condition.lower():
                    contraindication_alerts.append(f"Contraindication for {med['brand_name']}: {contra} (Patient has {condition}).")
                if "liver" in contra.lower() and "hepatic" in condition.lower():
                    contraindication_alerts.append(f"Contraindication for {med['brand_name']}: {contra} (Patient has {condition}).")

    # 2. Check Drug-Drug Interactions
    med_ids_set = set(req.medicine_ids)
    for rule in DRUG_INTERACTIONS_MATRIX:
        if rule["drugs"].issubset(med_ids_set):
            drug_names = [MEDICINES_CATALOG[m]["brand_name"] for m in rule["drugs"]]
            interaction_alerts.append(DrugInteractionAlert(
                drug_a=drug_names[0],
                drug_b=drug_names[1] if len(drug_names) > 1 else "Unknown",
                severity=rule["severity"],
                mechanism=rule["mechanism"],
                clinical_recommendation=rule["recommendation"],
            ))

    # 3. Check Duplicate Therapies
    seen_classes = {}
    for med in meds:
        tclass = med["therapeutic_class"]
        if tclass in seen_classes:
            duplicate_therapy_alerts.append(
                f"Duplicate Therapeutic Class: Both '{seen_classes[tclass]}' and '{med['brand_name']}' belong to '{tclass}'."
            )
        else:
            seen_classes[tclass] = med["brand_name"]

    # Compute overall risk level and score
    if allergy_alerts or any(ia.severity == "Critical" for ia in interaction_alerts):
        overall_risk = "Critical"
        risk_score = 92
        is_safe = False
    elif any(ia.severity == "High" for ia in interaction_alerts) or contraindication_alerts:
        overall_risk = "High"
        risk_score = 75
        is_safe = False
    elif any(ia.severity == "Moderate" for ia in interaction_alerts) or duplicate_therapy_alerts:
        overall_risk = "Medium"
        risk_score = 45
        is_safe = True
    else:
        overall_risk = "Normal"
        risk_score = 12
        is_safe = True

    return SafetyCheckResult(
        patient_id=req.patient_id,
        overall_risk_level=overall_risk,
        risk_score_100=risk_score,
        is_safe_to_dispense=is_safe,
        interaction_alerts=interaction_alerts,
        allergy_alerts=allergy_alerts,
        contraindication_alerts=contraindication_alerts,
        duplicate_therapy_alerts=duplicate_therapy_alerts,
        special_population_warnings=special_warnings,
    )
