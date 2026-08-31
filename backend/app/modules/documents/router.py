"""
MediCore Nexus - Document Management & Clinical Vault
Encrypted storage for medical charts, lab reports, ID proofs, and digital prescriptions
"""

from typing import List, Optional, Dict
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

class DocumentMetadata(BaseModel):
    id: str
    patient_id: str
    patient_name: str
    document_title: str
    document_type: str  # Lab Report, Discharge Summary, Imaging (DICOM/PDF), Consent Form, Insurance Card
    file_extension: str
    file_size_kb: int
    version: int = 1
    is_encrypted: bool = True
    uploaded_at: datetime
    uploaded_by: str

DOCUMENTS_STORE: List[Dict] = [
    {
        "id": "doc-vault-001",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "document_title": "Comprehensive Lipid Panel & Renal Report - Aug 2026",
        "document_type": "Lab Report",
        "file_extension": "PDF",
        "file_size_kb": 348,
        "version": 1,
        "is_encrypted": True,
        "uploaded_at": datetime.now(timezone.utc) - timedelta(days=3),
        "uploaded_by": "David Kim, MLS",
    },
    {
        "id": "doc-vault-002",
        "patient_id": "pat-001",
        "patient_name": "Eleanor Vance",
        "document_title": "Signed E-Prescription RX-2026-889101 (Cryptographically Verified)",
        "document_type": "Prescription",
        "file_extension": "PDF",
        "file_size_kb": 142,
        "version": 1,
        "is_encrypted": True,
        "uploaded_at": datetime.now(timezone.utc) - timedelta(days=2),
        "uploaded_by": "Dr. Sarah Chen, MD",
    }
]

router = APIRouter(prefix="/documents", tags=["Document Management"])

@router.get("", response_model=List[DocumentMetadata])
async def list_documents(patient_id: Optional[str] = None):
    if patient_id:
        return [d for d in DOCUMENTS_STORE if d["patient_id"] == patient_id]
    return DOCUMENTS_STORE
