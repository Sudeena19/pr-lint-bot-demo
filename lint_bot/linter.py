import os

def lint_file(filepath):
    issues = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if len(line) > 80:
            issues.append({"filename": filepath, "line": i, "message": "Line > 80 chars"})
        if line.rstrip() != line:
            issues.append({"filename": filepath, "line": i, "message": "Trailing whitespace"})
    return issues

def lint_repo(repo_path):
    all_issues = []
    for root, dirs, files in os.walk(repo_path):
        # Skip venv and cache folders
        if "venv" in root or "__pycache__" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))
    return all_issues
