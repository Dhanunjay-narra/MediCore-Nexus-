"""
MediCore Nexus - GitHub Pull Request Creator & Auto-Merger
Creates actual GitHub Pull Requests for all feature branches using GitHub REST API
and merges them so they appear in GitHub Web UI as Merged PRs.
"""

import subprocess
import requests
import json
import time

REPO = "Dhanunjay-narra/MediCore-Nexus-"
API_URL = f"https://api.github.com/repos/{REPO}"

def get_github_token():
    """Retrieve GitHub token from git credential helper."""
    proc = subprocess.Popen(
        ["git", "credential", "fill"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, _ = proc.communicate("protocol=https\nhost=github.com\n")
    token = None
    for line in out.splitlines():
        if line.startswith("password="):
            token = line.split("password=")[1].strip()
    return token

def test_api():
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    r = requests.get(API_URL, headers=headers)
    print(f"GitHub API connection status: {r.status_code}")
    if r.status_code == 200:
        print(f"Authenticated as: {r.json().get('full_name')}")
        return headers
    else:
        print(f"Error: {r.text}")
        return None

if __name__ == "__main__":
    test_api()
