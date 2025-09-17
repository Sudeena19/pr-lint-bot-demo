import os
import subprocess
import json

IGNORE_DIRS = {"venv", ".venv", "__pycache__", ".git"}


def lint_file(file_path):
    """
    Lint a single Python file using Ruff and return a list of issues.
    Each issue is a dict with keys: filename, line, message.
    """
    issues = []
    try:
        result = subprocess.run(
            ["ruff", "check", "--select=E,F,W", "--format=json", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout.strip()

        # DEBUG: print raw Ruff output
        print(f"DEBUG Ruff output for {file_path}: {output}")

        if output:
            try:
                ruff_issues = json.loads(output)
                for issue in ruff_issues:
                    issues.append({
                        "filename": issue.get("filename", file_path),
                        "line": issue.get("location", {}).get("row", 1),
                        "message": issue.get("message", "Linting issue")
                    })
            except json.JSONDecodeError as e:
                print(f"Could not parse Ruff output for {file_path}: {e}")
    except Exception as e:
        print(f"Error linting {file_path}: {e}")
    return issues


def lint_repo(repo_path="."):
    """
    Lint all Python files in the repository, ignoring cache/packaging dirs.
    Returns a list of all issues found.
    """
    all_issues = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f.endswith(".py"):
                file_path = os.path.join(root, f)
                all_issues.extend(lint_file(file_path))
    return all_issues
