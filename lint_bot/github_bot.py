import os
from github import Github

PAT_TOKEN = os.getenv("PAT_TOKEN")
REPO_NAME = os.getenv("REPO")
PR_NUMBER = int(os.getenv("PR_NUMBER", 0))

if not all([PAT_TOKEN, REPO_NAME, PR_NUMBER]):
    raise EnvironmentError("Missing environment variables: PAT_TOKEN, REPO, or PR_NUMBER")

gh = Github(PAT_TOKEN)
repo = gh.get_repo(REPO_NAME)
pr = repo.get_pull(PR_NUMBER)


def post_inline_comment(issue):
    """
    Try to post an inline comment on the PR for a single issue.
    """
    try:
        pr.create_review(
            event="COMMENT",
            comments=[{
                "path": issue["filename"],
                "position": issue["line"] if issue["line"] > 0 else 1,
                "body": issue["message"]
            }]
        )
        print(f"Inline comment posted: {issue['filename']}:{issue['line']}")
        return True
    except Exception as e:
        print(f"Could not post inline comment for {issue['filename']}:{issue['line']} -> {e}")
        return False


def post_summary_comment(issues):
    """
    Always posts a summary comment for all linting issues.
    """
    if not issues:
        body = "No linting issues found."
    else:
        body = "## Linting Summary\n"
        for issue in issues:
            body += f"- {issue['filename']}:{issue['line']} - {issue['message']}\n"

    try:
        pr.create_issue_comment(body)
        print("Summary comment posted.")
    except Exception as e:
        print(f"Could not post summary comment: {e}")
