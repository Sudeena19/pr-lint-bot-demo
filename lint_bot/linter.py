import os

def lint_file(file_path):
    """
    Lint a single Python file.
    Returns a list of issues with keys: filename, line, message.
    """
    issues = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if len(line) > 100:
                issues.append({
                    "filename": file_path,
                    "line": i,
                    "message": "Line exceeds 100 characters"
                })
            if "\t" in line:
                issues.append({
                    "filename": file_path,
                    "line": i,
                    "message": "Tab character found, use spaces instead"
                })
            if line.rstrip().endswith(" "):
                issues.append({
                    "filename": file_path,
                    "line": i,
                    "message": "Trailing whitespace"
                })
    return issues

def lint_repo(root_dir="."):
    """
    Lint all Python files in a directory recursively.
    Returns a list of all issues.
    """
    all_issues = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".py"):
                file_path = os.path.join(root, f)
                all_issues.extend(lint_file(file_path))
    return all_issues
