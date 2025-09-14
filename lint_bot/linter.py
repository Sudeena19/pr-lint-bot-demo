import os
import re

def lint_file(filename):
    issues = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines, start=1):
            if len(line) > 100:
                issues.append(f"{filename}:{i} Line too long ({len(line)} chars)")
            if "\t" in line:
                issues.append(f"{filename}:{i} Contains tab instead of spaces")
            if re.search(r"[ \t]+$", line.rstrip("\n\r")):
                issues.append(f"{filename}:{i} Trailing whitespace")
    except Exception:
        pass
    return issues

def lint_repo(path):
    all_issues = []
    for root, _, files in os.walk(path):
        if ".github" in root or "venv" in root or "__pycache__" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))
    return all_issues
