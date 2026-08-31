"""
Sync all feature branches with main and push to GitHub
"""

import subprocess

branches = [
    'feature/phase1-identity-security',
    'feature/phase2-hospital-organization',
    'feature/phase3-patient-care-emr',
    'feature/phase4-prescriptions-safety-lab',
    'feature/phase5-pharmacy-command-inventory',
    'feature/phase6-commerce-pos-insurance',
    'feature/phase7-telemedicine-notifications',
    'feature/phase8-ai-clinical-intelligence',
]

subprocess.run('git checkout main', shell=True)
subprocess.run('git pull origin main', shell=True)

for b in branches:
    print(f"Syncing branch {b}...")
    subprocess.run(f'git checkout {b}', shell=True)
    subprocess.run('git merge main -m "chore(sync): sync branch with main"', shell=True)
    subprocess.run(f'git push origin {b}', shell=True)

subprocess.run('git checkout main', shell=True)
print("All branches synced and pushed to remote successfully!")
