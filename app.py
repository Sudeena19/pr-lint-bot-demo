import os
import re
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")

API_URL = f"https://api.github.com/repos/{REPO}"

def lint_file(filename):
    issues = []
    with open(filename, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append((filename, i, f"Line too long ({len(line)} chars)"))
        if "\t" in line:
            issues.append((filename, i, "Contains tab instead of spaces"))
        if re.search(r"\s+$", line):
            issues.append((filename, i, "Trailing whitespace"))
    return issues

def get_pr_diff():
    """Fetch diff info for the PR to know valid positions for inline comments."""
    url = f"{API_URL}/pulls/{PR_NUMBER}/files"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {f["filename"]: f for f in response.json()}
    else:
        print("Failed to fetch PR files:", response.status_code, response.text)
        return {}

def comment_inline(issues, pr_files):
    """Try to comment inline if file + line exist in PR diff."""
    comments = []
    for filename, line, message in issues:
        if filename in pr_files:
            comments.append({
                "path": filename,
                "line": line,
                "side": "RIGHT",
                "body": message
            })
    if comments:
        url = f"{API_URL}/pulls/{PR_NUMBER}/reviews"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        data = {
            "body": "Linting issues found by PR Lint Bot",
            "event": "REQUEST_CHANGES",
            "comments": comments
        }
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            print("Inline comments posted successfully!")
        else:
            print("Failed inline comments:", r.status_code, r.text)
    return comments

def comment_summary(issues):
    """Fallback to summary comment if inline not possible."""
    url = f"{API_URL}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    body = "PR Lint Bot found the following issues:\n\n" + "\n".join(
        [f"{f}:{l} {msg}" for f, l, msg in issues]
    )
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Summary comment posted successfully!")
    else:
        print("Failed summary comment:", response.status_code, response.text)

if __name__ == "__main__":
    all_issues = []
    for root, _, files in os.walk("."):
        if ".github" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))

    if not all_issues:
        print("No issues found!")
        comment_summary([("N/A", 0, "No linting issues found!")])
    else:
        print("Issues found:")
        for issue in all_issues:
            print(issue)
        pr_files = get_pr_diff()
        inline_done = comment_inline(all_issues, pr_files)
        if not inline_done:
            comment_summary(all_issues)
