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
    Posts an inline comment on the pull request for a given issue.
    """
    try:
        commit_id = pr.head.sha  # commit on which PR is based
        pr.create_review_comment(
            body=issue["message"],
            commit_id=commit_id,
            path=issue["filename"],
            line=issue["line"]
        )
    except Exception as e:
        print(f"Could not post inline comment, will include in summary: {e}")


def post_summary_comment(issues):
    """
    Posts a summary comment listing all linting issues.
    """
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
