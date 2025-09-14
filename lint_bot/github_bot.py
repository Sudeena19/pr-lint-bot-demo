import os
from github import Github

def post_inline_comment(repo_name, pr_number, issues):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Missing GITHUB_TOKEN")
        return
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    for issue in issues:
        try:
            pr.create_review(
                body=issue["message"],
                event="COMMENT",
                comments=[{
                    "path": issue["filename"].replace("\\", "/"),
                    "position": issue["line"],
                    "body": issue["message"]
                }]
            )
        except Exception as e:
            print(f"Could not post inline comment, will include in summary: '{issue['message']}'")

def post_summary_comment(repo_name, pr_number, issues):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Missing GITHUB_TOKEN")
        return
    g = Github(token)
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    if not issues:
        body = " No lint issues found."
    else:
        body = " Lint issues summary:\n"
        for issue in issues:
            body += f"- {issue['filename']}:{issue['line']} - {issue['message']}\n"

    pr.create_issue_comment(body)
