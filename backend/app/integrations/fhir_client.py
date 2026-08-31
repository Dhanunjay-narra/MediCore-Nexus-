"""
MediCore Nexus - HL7 FHIR R4 Interoperability Connector
Facilitates standards-compliant health information exchange (HIE)
"""

from typing import Dict, Any, List
from datetime import datetime, timezone

class FHIRClient:
    """HL7 FHIR R4 Resource Serializer & Bridge"""

    @staticmethod
    def patient_to_fhir_resource(patient: Dict[str, Any]) -> Dict[str, Any]:
        """Convert internal Patient entity to standardized FHIR R4 Patient resource."""
        return {
            "resourceType": "Patient",
            "id": patient.get("id"),
            "identifier": [
                {
                    "system": "https://medicorenexus.io/mrn",
                    "value": patient.get("mrn"),
                }
            ],
            "name": [
                {
                    "use": "official",
                    "family": patient.get("last_name"),
                    "given": [patient.get("first_name")],
                }
            ],
            "telecom": [
                {"system": "phone", "value": patient.get("phone")},
                {"system": "email", "value": patient.get("email")},
            ],
            "gender": patient.get("gender", "unknown").lower(),
            "birthDate": patient.get("dob"),
            "address": [
                {
                    "line": [patient.get("address", "")],
                    "city": patient.get("city", ""),
                    "state": patient.get("state", ""),
                    "postalCode": patient.get("zip_code", ""),
                }
            ],
        }

    @staticmethod
    def prescription_to_fhir_medication_request(prescription: Dict[str, Any]) -> Dict[str, Any]:
        """Convert E-Prescription to FHIR R4 MedicationRequest resource."""
        return {
            "resourceType": "MedicationRequest",
            "id": prescription.get("id"),
            "status": "active",
            "intent": "order",
            "subject": {"reference": f"Patient/{prescription.get('patient_id')}"},
            "authoredOn": prescription.get("created_at", datetime.now(timezone.utc).isoformat()),
            "requester": {"reference": f"Practitioner/{prescription.get('doctor_id')}"},
            "dosageInstruction": [
                {
                    "text": item.get("instructions"),
                    "timing": {"code": {"text": item.get("frequency")}},
                    "route": {"text": item.get("route")},
                }
                for item in prescription.get("items", [])
            ],
        }
