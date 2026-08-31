"""
MediCore Nexus - Zip Archive Packager & TrainPlex Checker Evaluator
"""

import os
import zipfile
import requests
import json
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_FILENAME = "MediCore Nexus.zip"
ZIP_PATH = os.path.join(BASE_DIR, ZIP_FILENAME)
CHECKER_URL = "https://train-plex-checker-bot-1--ttejaswar1234.replit.app/api/check"

def make_zip():
    print(f"Creating archive {ZIP_FILENAME} at {ZIP_PATH}...")
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    excluded_dirs = {"node_modules", "dist", "dist-ssr", "__pycache__", ".pytest_cache", ".venv", "venv", ".idea", ".vscode"}
    excluded_extensions = {".pyc", ".pyo", ".pyd", ".zip"}

    file_count = 0
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file in files:
                if any(file.endswith(ext) for ext in excluded_extensions):
                    continue
                if file == ZIP_FILENAME:
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, BASE_DIR)
                zipf.write(full_path, rel_path)
                file_count += 1

    zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    print(f"Archive created with {file_count} files ({zip_size_mb:.2f} MB)")
    return ZIP_PATH

def evaluate_with_checker():
    zip_file_path = make_zip()
    print(f"\nUploading {ZIP_FILENAME} to TrainPlex Checker Bot: {CHECKER_URL}...")
    
    with open(zip_file_path, "rb") as f:
        files = {"file": (ZIP_FILENAME, f, "application/zip")}
        try:
            response = requests.post(CHECKER_URL, files=files, timeout=60)
        except Exception as e:
            print(f"Network error during upload: {e}")
            return None

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    return response.json()

def print_report(data):
    if not data:
        print("No evaluation data received.")
        return False

    tp = data.get("trainplex", {})
    summary = tp.get("summary", {})
    checks = tp.get("checks", [])

    print("\n" + "=" * 70)
    print("TRAINPLEX CHECKER EVALUATION REPORT")
    print("=" * 70)
    print(f"Overall Status: {summary.get('overall')}")
    print(f"Score:          {summary.get('score')}%")
    print(f"Total Checks:   {summary.get('total')}")
    print(f"Passed:         {summary.get('passed')}")
    print(f"Warnings:       {summary.get('warned')}")
    print(f"Failed:         {summary.get('failed')}")
    print(f"LOC:            {summary.get('loc')}")
    print(f"Commits:        {summary.get('git', {}).get('commits')}")
    print(f"PR Merges:      {summary.get('git', {}).get('prs')}")
    print("=" * 70)
    print("\nCHECKLIST BREAKDOWN:")
    for c in checks:
        status_tag = "[PASS]" if c.get("status") == "pass" else ("[WARN]" if c.get("status") == "warn" else "[FAIL]")
        name = str(c.get("name", "")).encode("ascii", "replace").decode("ascii")
        details = str(c.get("details", "")).encode("ascii", "replace").decode("ascii")
        value = str(c.get("value", "")).encode("ascii", "replace").decode("ascii")
        print(f"{status_tag} {name}: {details} (Value: {value})")
        if c.get("status") != "pass" and c.get("fix"):
            fix_hint = str(c.get("fix", "")).encode("ascii", "replace").decode("ascii")
            print(f"   -> Fix Hint: {fix_hint}")

    is_perfect = (summary.get("score") == 100 or summary.get("overall") == "READY") and summary.get("failed") == 0
    return is_perfect

if __name__ == "__main__":
    result_data = evaluate_with_checker()
    success = print_report(result_data)
    if success:
        print("\nSUCCESS: 100% / READY achieved on TrainPlex Checker!")
        sys.exit(0)
    else:
        print("\nNeeds fixes to achieve 100% pass.")
        sys.exit(1)
