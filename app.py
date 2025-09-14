import os
import re
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Sudeena19/pr-lint-bot"
PR_NUMBER = os.getenv("PR_NUMBER")

# Ensure a demo bad file exists for testing
if not os.path.exists("bad_code.py"):
    with open("bad_code.py", "w") as f:
        f.write("def example():    \n\tprint('Hello World!')  # tab + long line for demo\n")

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

def comment_on_pr(issues):
    if not GITHUB_TOKEN or not PR_NUMBER:
        print("Missing GitHub token or PR number, cannot post comment.")
        return
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    body = "PR Lint Bot found the following issues:\n\n" + "\n".join(issues)
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Comment posted successfully!")
    else:
        print("Failed to post comment:", response.status_code, response.text)

if __name__ == "__main__": 
    all_issues = []
    for root, _, files in os.walk("."):
        if ".github" in root:
            continue  # skip workflow files
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))

    if all_issues:
        print("Issues found:")
        for issue in all_issues:
            print(issue)
        comment_on_pr(all_issues)
    else:
        print("No issues found!")
