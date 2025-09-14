import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

def post_summary_comment(messages):
    if not GITHUB_TOKEN or not REPO or not PR_NUMBER:
        print("Missing environment variables for GitHub bot")
        return
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    body = "\n".join(messages)
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Summary comment posted successfully!")
    else:
        print("Failed to post summary:", response.status_code, response.text)

def post_inline_comment(file, line, message):
    # GitHub PR review comments require a proper GitHub App token with permissions.
    # For simplicity, this workflow will post only a summary comment for all issues.
    print(f"Inline comment: {file}:{line} {message}")
