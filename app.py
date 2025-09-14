import os
import re
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")  
PR_NUMBER = os.getenv("PR_NUMBER")

def lint_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append(f"{filename}:{i} Line too long ({len(line)} chars)")
        if "\t" in line:
            issues.append(f"{filename}:{i} Contains tab instead of spaces")
        if re.search(r"\s+$", line):
            issues.append(f"{filename}:{i} Trailing whitespace")
    return issues

def comment_on_pr(messages):
    if not GITHUB_TOKEN or not PR_NUMBER:
        print("Missing GitHub token or PR number, cannot post comment.")
        return
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    body = "\n".join(messages)
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print("Failed to post comment:", response.status_code, response.text)

if __name__ == "__main__": 
    all_issues = []
    for root, _, files in os.walk("."):
        if ".github" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))

    if all_issues:
        print("Issues found:")
        for issue in all_issues:
            print(issue)
        comment_on_pr([" Linting issues found:"] + all_issues)
    else:
        print("No issues found!")
        comment_on_pr(["No linting issues found!"])