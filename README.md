# MediCore Nexus
> **Integrated Pharmacy, Hospital & Patient Care Management Platform**

MediCore Nexus is a comprehensive, enterprise-grade healthcare operations platform designed with an advanced pharmacy-first clinical architecture. It seamlessly integrates hospital management, patient care, electronic medical records (EMR), e-prescriptions, laboratory workflows, billing, insurance adjudication, telemedicine, and AI-assisted clinical decision support.

---

## Architecture Overview

```
                      ┌─────────────────────────────────┐
                      │    MediCore Nexus Frontend      │
                      │       React / TypeScript        │
                      └────────────────┬────────────────┘
                                       │
                      ┌────────────────▼────────────────┐
                      │        FastAPI Gateway          │
                      │ Authentication / Routing / RBAC │
                      └────────────────┬────────────────┘
                                       │
       ┌───────────────────────────────┼───────────────────────────────┐
       │                               │                               │
       ▼                               ▼                               ▼
 Patient Services              Pharmacy Services               Clinical Services
  - Patients Master Index       - Medicine Catalog (Master)     - Doctor Management
  - Appointments & Queues       - Inventory & Batch Tracking    - Electronic Medical Records (EMR)
  - Medical History Timeline    - Smart FEFO Dispensing         - E-Prescriptions & QR Codes
  - Consent & Emergency Info    - Supply Chain & Procurement    - Laboratory & Critical Alerts
       │                               │                               │
       └───────────────────────────────┼───────────────────────────────┘
                                       │
                      ┌────────────────▼────────────────┐
                      │         Shared Engines          │
                      │  - Drug Safety & Risk Radar     │
                      │  - Predictive Stock Forecaster  │
                      │  - Billing & Revenue Ledger     │
                      │  - Insurance Claims Engine      │
                      │  - Telemedicine Suite           │
                      │  - Audit & Compliance Logging   │
                      └────────────────┬────────────────┘
                                       │
             ┌─────────────────────────┼─────────────────────────┐
             ▼                         ▼                         ▼
        PostgreSQL / SQLite          Redis Cache/Queue       Document Storage
        Primary Relational DB        PubSub & Task Engine     Encrypted Documents
```

---

## Key System Modules & Domains

MediCore Nexus is divided into 24 distinct domain modules to prevent tight coupling and ensure independent scalability:

1. **Identity & Access Management**: JWT authentication, refresh tokens, MFA simulation, password hashing, account lockout protection, and role-based access control across 14 specialized healthcare roles.
2. **Organization & Hospital Management**: Multi-hospital hierarchies, branches, departments, wards, rooms, inpatient beds, consultation units, and pharmacy counters.
3. **Patient Management**: Central Master Patient Index (MPI), demographics, allergies, chronic conditions, guardian information, deduplication, and timeline.
4. **Doctor Management**: Physician directory, medical licenses, specializations, consultation fee tiers, hospital/department assignments, and working schedules.
5. **Appointment Management**: Doctor availability slots, walk-in bookings, queue management, status lifecycle (Booked -> Confirmed -> Checked-In -> In-Consultation -> Completed), and no-show tracking.
6. **Electronic Medical Records (EMR)**: Longitudinal clinical chart, encounter notes (SOAP format), vitals tracking, ICD-10 diagnoses, immunization records, and discharge summaries.
7. **Prescription Management**: Electronic prescriptions, digital signatures, refill tracking, QR code verification, dosage calculations, and pharmacist dispensing history.
8. **Medicine Catalog Master**: Drug master catalog separated from physical stock, generic/brand mappings, dosage forms, therapeutic classifications, contraindications, and barcode identifiers.
9. **Pharmacy Inventory Management**: Multi-warehouse & shelf management, lot/batch tracking, expiry date monitoring, low-stock alerts, and stock adjustments.
10. **Supplier & Procurement**: Vendor profiles, procurement contracts, purchase requisitions, multi-level purchase order approvals, and goods receipt tracking.
11. **Pharmacy Sales & POS**: High-throughput point-of-sale, barcode scanning, OTC & prescription-based checkout, split payments, and instant receipt generation.
12. **Drug Safety & Clinical Pharmacy**: Multi-tier drug-drug interaction engine, drug-allergy checking, duplicate therapy warnings, renal dosage alerts, and pregnancy risk classification.
13. **Laboratory Management**: Test packages, doctor lab orders, sample barcode generation, multi-stage processing, reference ranges, and critical value notifications.
14. **Billing & Revenue Management**: Unified invoice ledger, automated fee calculations for consultations, lab orders, pharmacy sales, and multi-currency payments.
15. **Insurance Management**: Payer directory, patient insurance policies, eligibility verification, pre-authorization, claims lifecycle, deductibles, and co-pay adjudication.
16. **Telemedicine**: Virtual appointments, simulated WebRTC video rooms, in-call clinical note synchronization, instant e-prescriptions, and encrypted chat.
17. **Pharmacy Staff Management**: Staff rostering, duty shifts, attendance tracking, counter assignments, and performance metrics.
18. **Healthcare & Pharmacy Analytics**: Real-time business intelligence, daily/monthly sales volume, top grossing medicines, slow-moving inventory, doctor utilization, and no-show rates.
19. **AI Clinical Decision Support**: Rule-based & ML inference engine for prescription anomalies, dosage verification, and clinical safety risk grading.
20. **AI Predictive Inventory**: Daily burn rate calculations, stock-out estimation, reorder quantity forecasting, and seasonal demand predictions.
21. **AI Natural Language Analytics**: Conversational query engine for operational reporting and financial intelligence.
22. **Audit, Compliance & Security**: Immutable audit trail, field-level access tracking, medical record access logs, IP logging, and compliance reporting.
23. **Document Management**: Encrypted clinical documents, lab reports, ID proofs, insurance cards, and digital signature archives.
24. **Multi-Channel Notifications**: SMS, Email, WhatsApp, and in-app alert notifications for appointment reminders, low stock, and critical lab values.

---

## 14 System Roles & Permissions

- **Super Admin**: Complete platform configuration, global settings, and audit logs.
- **Hospital Admin**: Hospital operations, department structuring, and staff allocation.
- **Pharmacy Admin**: Pharmacy inventory, procurement policies, and pricing rules.
- **Doctor**: Consultations, clinical notes, diagnosis, e-prescribing, and lab orders.
- **Pharmacist**: Prescription validation, FEFO batch selection, dispensing, and safety reviews.
- **Pharmacy Technician**: Stock receiving, shelf organization, and POS cashiering.
- **Nurse**: Patient vitals entry, triage, bed management, and doctor assistance.
- **Lab Technician**: Sample collection, test processing, and lab results entry.
- **Billing Officer**: Invoice generation, payments processing, and refund reconciliation.
- **Insurance Officer**: Policy validation, pre-authorizations, and claims adjudication.
- **Receptionist**: Patient check-in, appointment booking, and queue management.
- **Patient**: Personal portal, appointment history, prescriptions, and lab reports.
- **Supplier**: Purchase order fulfillment and delivery scheduling.
- **Auditor**: Read-only compliance inspection and security audit tracking.

---

## Prerequisites

- **Python**: Version 3.11+ or 3.12+
- **Node.js**: Version 18.x or 20.x LTS
- **npm**: Version 9.x or 10.x
- **Git**: Version 2.30+
- **Docker & Docker Compose** (Optional, for containerized execution)

---

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Dhanunjay-narra/MediCore-Nexus-.git
cd MediCore-Nexus-
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
# Install node dependencies
npm install
```

---

## Build

### Frontend Production Build
```bash
npm run build
```
This builds optimized client assets into the `dist/` directory.

### Container Build
```bash
docker build -t medicore-nexus:latest .
```

---

## Run

### Development Mode

#### Start Backend Service:
```bash
# Using uvicorn
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Interactive API Swagger Docs: `http://127.0.0.1:8000/docs`

#### Start Frontend Application:
```bash
npm run dev
```
Access Frontend UI: `http://localhost:5173`

### Production Mode with Docker Compose
```bash
docker-compose up -d
```

---

## Testing

MediCore Nexus includes comprehensive automated test suites covering all domains:

```bash
# Run backend pytest suite
pytest -v tests/

# Run frontend tests
npm test
```

---

## Deployment & Kubernetes

Kubernetes manifests are structured in the `k8s/` directory for deployment to cloud clusters:
- `k8s/namespace.yaml`
- `k8s/backend-deployment.yaml`
- `k8s/frontend-deployment.yaml`
- `k8s/postgres-statefulset.yaml`
- `k8s/redis-deployment.yaml`
- `k8s/ingress.yaml`

Deploy with kubectl:
```bash
kubectl apply -f k8s/
```

---

## API Documentation

The RESTful API provides over 50 structured endpoints versioned under `/api/v1/`:
- `GET /api/v1/health` - Health check & uptime status
- `POST /api/v1/auth/login` - User authentication & JWT issuance
- `GET /api/v1/patients` - List and filter patient records
- `POST /api/v1/prescriptions` - Create structured e-prescription
- `POST /api/v1/drug-safety/check` - Clinical drug-drug & allergy safety validation
- `GET /api/v1/inventory/fefo-recommendation` - Smart FEFO batch allocation
- `POST /api/v1/sales/checkout` - Pharmacy POS transaction & stock deduction
- `GET /api/v1/analytics/pharmacy/command-center` - Real-time operational metrics
- `POST /api/v1/ai/clinical-decision-support` - AI clinical insights & risk analysis

---

## License & Ownership

**Proprietary Commercial Software**  
Copyright (c) 2026 **Dhanunjay Narra**. All Rights Reserved.  
Confidential and proprietary. See [LICENSE](LICENSE) for details.
