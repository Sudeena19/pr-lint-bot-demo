import os
import re
from github import Github

def lint_file(filename):
    issues = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append((filename, i, f"Line too long ({len(line)} chars)"))
        if "\t" in line:
            issues.append((filename, i, "Contains tab instead of spaces"))
        if re.search(r"[ \t]+$", line.rstrip("\n\r")):
            issues.append((filename, i, "Trailing whitespace"))
    return issues

def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("PR_NUMBER"))

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    issues = []
    for file in pr.get_files():
        if file.filename.endswith(".py"):
            issues.extend(lint_file(file.filename))

    for file, line, msg in issues:
        pr.create_review_comment(
            body=msg,
            commit_id=pr.head.sha,
            path=file,
            line=line,
            side="RIGHT"
        )

if __name__ == "__main__":
    main()