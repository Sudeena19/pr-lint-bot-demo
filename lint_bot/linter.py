import subprocess
import json
import os

SERIOUS_CODES = {"E", "F", "W"}  # Example: E=error, F=failed, W=warning
# You can adjust based on ruff's code convention

def lint_file(filepath):
    """Lint a single Python file and return issues"""
    issues = []
    try:
        result = subprocess.run(
            ["ruff", "--format", "json", filepath],
            capture_output=True,
            text=True,
            check=False
        )
        if result.stdout:
            data = json.loads(result.stdout)
            for item in data:
                code_prefix = item["code"][0] if "code" in item else "?"
                issues.append({
                    "filename": os.path.relpath(item["filename"]),
                    "line": item.get("line", 0),
                    "message": item.get("message", ""),
                    "serious": code_prefix in SERIOUS_CODES
                })
    except Exception as e:
        issues.append({
            "filename": filepath,
            "line": 0,
            "message": f"Failed to lint file: {str(e)}",
            "serious": True
        })
    return issues

def lint_repo(repo_path="."):
    """Lint all Python files in repo"""
    all_issues = []
    for root, _, files in os.walk(repo_path):
        for f in files:
            if f.endswith(".py"):
                filepath = os.path.join(root, f)
                all_issues.extend(lint_file(filepath))
    return all_issues
