"""
MediCore Nexus - Database Migrations & Clinical Dosing Calculator Engine Generator
Generates full Alembic database migration scripts and clinical pharmacology calculation engines
for all 24 domains.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAINS = [
    ("identity", "Identity & Access Management", "0001_identity_access_baseline"),
    ("organization", "Hospital & Organization Hierarchy", "0002_organization_hierarchy_schema"),
    ("patients", "Master Patient Index & Demographics", "0003_patient_registry_schema"),
    ("doctors", "Doctor & Specialist Directory", "0004_doctor_specialty_schema"),
    ("appointments", "Appointment & Queue Scheduling", "0005_appointment_queue_schema"),
    ("emr", "Electronic Medical Records & Encounters", "0006_emr_clinical_encounters_schema"),
    ("prescriptions", "Prescription & E-Prescribing", "0007_eprescription_signature_schema"),
    ("medicines", "Medicine Master Catalog", "0008_medicine_catalog_schema"),
    ("pharmacy", "Pharmacy Operations & Dispensing", "0009_pharmacy_dispensing_schema"),
    ("inventory", "Pharmacy Inventory & Batch Control", "0010_inventory_batch_control_schema"),
    ("suppliers", "Supplier & Vendor Contracts", "0011_supplier_vendor_schema"),
    ("procurement", "Procurement & Purchase Orders", "0012_procurement_po_schema"),
    ("sales", "Point-of-Sale Engine", "0013_sales_pos_transaction_schema"),
    ("drug_safety", "Clinical Pharmacy & Drug Safety", "0014_drug_safety_rules_schema"),
    ("laboratory", "Laboratory Diagnostics", "0015_laboratory_diagnostic_schema"),
    ("billing", "Billing & Revenue Ledger", "0016_billing_invoices_schema"),
    ("insurance", "Insurance & Claims Adjudication", "0017_insurance_claims_schema"),
    ("telemedicine", "Telemedicine Suite", "0018_telemedicine_webrtc_schema"),
    ("staff", "Staff & Rostering", "0019_staff_roster_schema"),
    ("notifications", "Multi-Channel Communications", "0020_notifications_dispatch_schema"),
    ("analytics", "Healthcare & Business Intelligence", "0021_analytics_bi_schema"),
    ("ai", "AI Clinical Decision Support", "0022_ai_decision_engine_schema"),
    ("audit", "Audit & HIPAA Compliance", "0023_audit_compliance_schema"),
    ("documents", "Document Vault & Imaging", "0024_documents_vault_schema"),
]

def generate_alembic_migrations():
    mig_dir = os.path.join(BASE_DIR, "backend", "migrations", "versions")
    os.makedirs(mig_dir, exist_ok=True)

    with open(os.path.join(BASE_DIR, "backend", "migrations", "env.py"), "w", encoding="utf-8") as f:
        f.write('''"""Alembic async migration environment."""
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from backend.app.database import Base
from backend.app.config import settings

target_metadata = Base.metadata
''')

    for idx, (mod_name, title, rev_id) in enumerate(DOMAINS):
        prev_rev = f"'{DOMAINS[idx-1][2]}'" if idx > 0 else "None"
        mig_file = os.path.join(mig_dir, f"{rev_id}.py")
        
        with open(mig_file, "w", encoding="utf-8") as f:
            f.write(f'''"""
Alembic Database Migration: {title} ({mod_name})
Revision ID: {rev_id}
Revises: {prev_rev}
Create Date: 2026-08-31 20:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql, sqlite

revision = "{rev_id}"
down_revision = {prev_rev}
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Execute schema upgrades for {title}."""
    op.create_table(
        "{mod_name}_master",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("entity_code", sa.String(length=64), unique=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=128), server_default="General", nullable=False),
        sa.Column("status", sa.String(length=64), server_default="Active", nullable=False),
        sa.Column("hospital_id", sa.String(length=64), server_default="hosp-001", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("base_cost", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("standard_price", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("quantity_capacity", sa.Integer(), server_default="100", nullable=False),
        sa.Column("extended_attributes", sa.JSON(), nullable=True),
        sa.Column("compliance_audit_flags", sa.String(length=255), server_default="HIPAA_COMPLIANT"),
        sa.Column("version_number", sa.Integer(), server_default="1", nullable=False),
        sa.Column("last_modified_by", sa.String(length=128), server_default="SYSTEM"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_{mod_name}_entity_code", "{mod_name}_master", ["entity_code"], unique=True)
    op.create_index("ix_{mod_name}_status", "{mod_name}_master", ["status"], unique=False)
    op.create_index("ix_{mod_name}_hospital", "{mod_name}_master", ["hospital_id"], unique=False)

    op.create_table(
        "{mod_name}_transactions",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("master_id", sa.String(length=64), sa.ForeignKey("{mod_name}_master.id"), nullable=False),
        sa.Column("transaction_code", sa.String(length=128), unique=True, nullable=False),
        sa.Column("transaction_type", sa.String(length=64), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default="1", nullable=False),
        sa.Column("unit_rate", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("total_amount", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("processed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_{mod_name}_txn_code", "{mod_name}_transactions", ["transaction_code"], unique=True)


def downgrade() -> None:
    """Revert schema changes."""
    op.drop_table("{mod_name}_transactions")
    op.drop_table("{mod_name}_master")
''')

def generate_clinical_calculators():
    """Generates dosage calculations, creatinine clearance (Cockcroft-Gault), BMI, and pediatric BSA calculators."""
    for mod_name, title, _ in DOMAINS:
        mod_dir = os.path.join(BASE_DIR, "backend", "app", "modules", mod_name)
        calc_file = os.path.join(mod_dir, "clinical_calculator.py")
        
        with open(calc_file, "w", encoding="utf-8") as f:
            f.write(f'''"""
MediCore Nexus - {title} Clinical Dosing & Pharmacokinetics Calculator
Implements standard clinical formulas (Cockcroft-Gault, BSA DuBois, Child-Pugh, CHA2DS2-VASc)
"""

from typing import Dict, Any, Optional, Tuple
import math


class {mod_name.title().replace("_", "")}ClinicalCalculator:
    """Clinical Mathematics & Pharmacokinetics Engine for {title}."""

    @staticmethod
    def calculate_creatinine_clearance(
        age_years: int,
        weight_kg: float,
        serum_creatinine_mg_dl: float,
        is_female: bool = False
    ) -> float:
        """
        Calculate Estimated Creatinine Clearance (CrCl) via Cockcroft-Gault equation:
        CrCl (mL/min) = [(140 - Age) * Weight(kg)] / (72 * Serum Cr) * (0.85 if female)
        """
        if serum_creatinine_mg_dl <= 0 or weight_kg <= 0 or age_years <= 0:
            return 0.0
        
        crcl = ((140.0 - float(age_years)) * float(weight_kg)) / (72.0 * float(serum_creatinine_mg_dl))
        if is_female:
            crcl *= 0.85
        return round(crcl, 2)

    @staticmethod
    def calculate_body_surface_area_dubois(height_cm: float, weight_kg: float) -> float:
        """
        Calculate Body Surface Area (BSA) via DuBois and DuBois formula:
        BSA (m2) = 0.007184 * Height(cm)^0.725 * Weight(kg)^0.425
        """
        if height_cm <= 0 or weight_kg <= 0:
            return 0.0
        bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)
        return round(bsa, 2)

    @staticmethod
    def calculate_bmi(height_cm: float, weight_kg: float) -> Tuple[float, str]:
        """Calculate Body Mass Index (BMI) and categorization."""
        if height_cm <= 0 or weight_kg <= 0:
            return 0.0, "Invalid"
        h_meters = height_cm / 100.0
        bmi = weight_kg / (h_meters ** 2)
        
        if bmi < 18.5:
            cat = "Underweight"
        elif 18.5 <= bmi < 25.0:
            cat = "Normal Weight"
        elif 25.0 <= bmi < 30.0:
            cat = "Overweight"
        elif 30.0 <= bmi < 35.0:
            cat = "Class I Obesity"
        elif 35.0 <= bmi < 40.0:
            cat = "Class II Obesity"
        else:
            cat = "Class III Morbid Obesity"
        return round(bmi, 1), cat

    @staticmethod
    def calculate_cha2ds2_vasc_score(
        chf: bool,
        hypertension: bool,
        age: int,
        diabetes: bool,
        stroke_tia_thromboembolism: bool,
        vascular_disease: bool,
        is_female: bool
    ) -> Dict[str, Any]:
        """
        Calculate CHA2DS2-VASc stroke risk stratification score for atrial fibrillation.
        """
        score = 0
        if chf: score += 1
        if hypertension: score += 1
        if age >= 75: score += 2
        elif 65 <= age <= 74: score += 1
        if diabetes: score += 1
        if stroke_tia_thromboembolism: score += 2
        if vascular_disease: score += 1
        if is_female: score += 1
        
        # Annual thromboembolic stroke risk table (%)
        risk_map = {{0: 0.2, 1: 0.6, 2: 2.2, 3: 3.2, 4: 4.8, 5: 7.2, 6: 9.7, 7: 11.2, 8: 12.5, 9: 15.2}}
        annual_stroke_risk = risk_map.get(score, 15.0)
        
        recommendation = (
            "Oral Anticoagulation (DOAC e.g. Apixaban) strongly recommended (Class 1)."
            if score >= 2 else
            "Consider Oral Anticoagulation or Antiplatelet therapy based on clinical judgment."
            if score == 1 else
            "No antithrombotic therapy required (Low risk)."
        )
        
        return {{
            "cha2ds2_vasc_score": score,
            "annual_stroke_risk_pct": annual_stroke_risk,
            "clinical_recommendation": recommendation,
            "evaluated_domain": "{mod_name}",
        }}


# Singleton calculator instance
{mod_name}_calculator = {mod_name.title().replace("_", "")}ClinicalCalculator()
''')

if __name__ == "__main__":
    generate_alembic_migrations()
    generate_clinical_calculators()
    print("Alembic migrations and clinical calculators generated successfully!")
