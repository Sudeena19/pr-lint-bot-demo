import os
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO")
PR_NUMBER = int(os.getenv("PR_NUMBER", 0))

if not all([GITHUB_TOKEN, REPO_NAME, PR_NUMBER]):
    raise EnvironmentError("Missing environment variables: GITHUB_TOKEN, REPO, or PR_NUMBER")

gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)
pr = repo.get_pull(PR_NUMBER)

def post_inline_comment(issue):
    try:
        pr.create_review(
            event="COMMENT",
            comments=[{
                "path": issue["filename"],
                "position": issue["line"] if issue["line"] > 0 else 1,
                "body": issue["message"]
            }]
        )
    except Exception as e:
        print(f"Could not post inline comment, will include in summary: {e}")

def post_summary_comment(issues):
    if not issues:
        body = "No linting issues found."
    else:
        body = "## Linting Summary\n"
        for issue in issues:
            body += f"- {issue['filename']}:{issue['line']} - {issue['message']}\n"
    try:
        pr.create_issue_comment(body)
    except Exception as e:
        print(f"Could not post summary comment: {e}")
