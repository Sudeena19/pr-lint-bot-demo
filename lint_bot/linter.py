import os

def lint_file(file_path):
    """Check a single file for linting issues."""
    issues = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append({"file": file_path, "line": i, "msg": "Line exceeds 100 characters"})
        if "\t" in line:
            issues.append({"file": file_path, "line": i, "msg": "Tab character found (use spaces)"})

    return issues


def lint_repo(path="."):
    """Lint all .py files in a repo."""
    all_issues = []
    for root, _, files in os.walk(path):
        if "site-packages" in root or ".venv" in root or "venv" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))
    return all_issues
