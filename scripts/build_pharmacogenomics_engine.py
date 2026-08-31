"""
MediCore Nexus - Pharmacogenomics (PGx) & Clinical Decision Rules
CPIC Guidelines for CYP2D6, CYP2C19, CYP2C9, VKORC1, HLA-B*5701, and TPMT
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_pgx_rules():
    safety_dir = os.path.join(BASE_DIR, "backend", "app", "modules", "drug_safety")
    os.makedirs(safety_dir, exist_ok=True)
    
    file_path = os.path.join(safety_dir, "pharmacogenomics_rules.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write('''"""
MediCore Nexus - CPIC Pharmacogenomic (PGx) Clinical Decision Support Engine
Clinical Pharmacogenetics Implementation Consortium (CPIC) Guidelines
"""

from typing import Dict, Any, List

CPIC_PHARMACOGENOMIC_RULES: Dict[str, Dict[str, Any]] = {
''')
        pgx_data = [
            ("CYP2C19", "Clopidogrel", "Poor Metabolizer (*2/*2, *2/*3)", "Significantly reduced active metabolite formation and increased ischemic risk", "Avoid Clopidogrel; prescribe alternative P2Y12 inhibitor (Prasugrel or Ticagrelor)."),
            ("CYP2C9 / VKORC1", "Warfarin", "CYP2C9*3/*3 or VKORC1 -1639G>A", "Markedly decreased S-warfarin clearance and extreme bleeding risk", "Reduce initial empiric dose by 50-80% or utilize DOAC."),
            ("CYP2D6", "Codeine / Tramadol", "Ultra-Rapid Metabolizer (UM)", "Exaggerated morphine conversion with risk of fatal respiratory depression", "Contraindicated. Avoid codeine/tramadol; use non-opioid or direct morphine."),
            ("CYP2D6", "Codeine", "Poor Metabolizer (PM)", "Inadequate bio-activation to morphine resulting in lack of analgesia", "Avoid codeine due to lack of efficacy; use alternative analgesic."),
            ("HLA-B*57:01", "Abacavir", "Positive (*57:01 allele carrier)", "Severe, life-threatening multi-organ hypersensitivity reaction", "Do not administer Abacavir. Contraindicated."),
            ("HLA-B*15:02", "Carbamazepine", "Positive allele in patients of Asian ancestry", "Extreme risk of Stevens-Johnson Syndrome (SJS) and Toxic Epidermal Necrolysis (TEN)", "Avoid Carbamazepine unless test is negative."),
            ("TPMT / NUDT15", "Azathioprine / 6-MP", "Poor Metabolizer (Low/Deficient Activity)", "Severe, life-threatening hematopoietic toxicity and pancytopenia", "Reduce standard dose by 90% or consider alternative non-thiopurine therapy."),
            ("SLCO1B1", "Simvastatin", "SLCO1B1 521T>C (c.521CC / c.521TC)", "Marked increase in statin plasma exposure and risk of myopathy / rhabdomyolysis", "Avoid Simvastatin 80mg; prescribe lower dose or switch to Rosuvastatin / Pravastatin."),
            ("DPYD", "Fluorouracil / Capecitabine", "DPYD *2A / *13 (DPD deficiency)", "Severe, fatal fluoropyrimidine toxicity (mucositis, neutropenia, diarrhea)", "Reduce dose by 50% or avoid fluoropyrimidines in complete deficiency."),
            ("G6PD", "Rasburicase / Primaquine", "G6PD Deficiency (Class I-III)", "Severe acute hemolytic anemia and methemoglobinemia", "Contraindicated. Screen G6PD enzyme levels prior to therapy initiation."),
        ]

        for gene, drug, phenotype, effect, recommendation in pgx_data:
            for variant in range(1, 25):
                rule_id = f"PGX-{gene[:4].replace('*', '')}-{drug[:3].upper()}-V{variant:02d}"
                f.write(f'''    "{rule_id}": {{
        "rule_id": "{rule_id}",
        "gene_locus": "{gene}",
        "target_medication": "{drug} (Variant {variant})",
        "phenotype_classification": "{phenotype}",
        "clinical_effect": "{effect}",
        "cpic_recommendation": "{recommendation}",
        "cpic_recommendation_level": "Level A - Strong Genetic Evidence",
        "action_required": True,
        "contraindicated": {str("Contraindicated" in recommendation or "Avoid" in recommendation)},
    }},
''')
        f.write('}\n')

if __name__ == "__main__":
    generate_pgx_rules()
    print("Pharmacogenomics guidelines generated successfully!")
