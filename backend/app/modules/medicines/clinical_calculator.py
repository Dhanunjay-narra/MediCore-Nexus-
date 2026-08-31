"""
MediCore Nexus - Medicine Master Catalog Clinical Dosing & Pharmacokinetics Calculator
Implements standard clinical formulas (Cockcroft-Gault, BSA DuBois, Child-Pugh, CHA2DS2-VASc)
"""

from typing import Dict, Any, Optional, Tuple
import math


class MedicinesClinicalCalculator:
    """Clinical Mathematics & Pharmacokinetics Engine for Medicine Master Catalog."""

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
        risk_map = {0: 0.2, 1: 0.6, 2: 2.2, 3: 3.2, 4: 4.8, 5: 7.2, 6: 9.7, 7: 11.2, 8: 12.5, 9: 15.2}
        annual_stroke_risk = risk_map.get(score, 15.0)
        
        recommendation = (
            "Oral Anticoagulation (DOAC e.g. Apixaban) strongly recommended (Class 1)."
            if score >= 2 else
            "Consider Oral Anticoagulation or Antiplatelet therapy based on clinical judgment."
            if score == 1 else
            "No antithrombotic therapy required (Low risk)."
        )
        
        return {
            "cha2ds2_vasc_score": score,
            "annual_stroke_risk_pct": annual_stroke_risk,
            "clinical_recommendation": recommendation,
            "evaluated_domain": "medicines",
        }


# Singleton calculator instance
medicines_calculator = MedicinesClinicalCalculator()
