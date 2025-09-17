import os
import subprocess

IGNORE_DIRS = {"venv", ".venv", "__pycache__", ".git"}


def lint_file(file_path):
    """
    Lint a single Python file using Ruff and return a list of issues.
    Each issue is a dict with keys: filename, line, message.
    """
    issues = []
    try:
        result = subprocess.run(
            ["ruff", "--select=E,F,W", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        output = result.stdout.strip()
        if output:
            for line in output.splitlines():
                # Ruff output format: path:line:col: code message
                parts = line.split(":", 3)
                if len(parts) == 4:
                    filename, line_no, _, message = parts
                    issues.append({
                        "filename": filename.strip(),
                        "line": int(line_no.strip()),
                        "message": message.strip()
                    })
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
