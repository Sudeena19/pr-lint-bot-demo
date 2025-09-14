import requests

def post_inline_comment(repo, pr_number, token, message):
    # For demonstration, just posts the first issue inline (needs line/commit info for true inline)
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    body = f"**PR Lint Bot Inline Example:** {message}"
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Inline comment posted!")
    else:
        print("Failed to post inline comment:", response.text)

def post_summary_comment(repo, pr_number, token, messages):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    body = "### PR Lint Bot Summary\n\n" + "\n".join(messages)
    response = requests.post(url, json={"body": body}, headers=headers)
    if response.status_code == 201:
        print("Summary comment posted!")
    else:
        print("Failed to post summary:", response.text)
