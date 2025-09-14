import os
import re
from github import Github

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))

def lint_file(filename):
    issues = []
    with open(filename, "r") as f:
        for i, line in enumerate(f, start=1):
            if len(line) > 100:
                issues.append((filename, i, f"Line too long ({len(line)} chars)"))
            if "\t" in line:
                issues.append((filename, i, "Contains tab instead of spaces"))
            if re.search(r"[ \t]+$", line.rstrip("\n\r")):
                issues.append((filename, i, "Trailing whitespace"))
    return issues

def main():
    gh = Github(auth=("token", token))
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    all_issues = []
    for root, _, files in os.walk("."):
        if ".github" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))

    if all_issues:
        commit = pr.get_commits().reversed[0]  # latest commit object
        for filename, line, msg in all_issues:
            pr.create_review_comment(
                body=msg,
                commit=commit,
                path=filename,
                line=line,
                side="RIGHT"
            )
        print("Inline comments added for lint issues!")
    else:
        pr.create_issue_comment("No linting issues found!")
        print("No issues found!")

if __name__ == "__main__":
    main()
