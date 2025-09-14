import os
from github import Github

def get_github_instance():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN not found in environment")
    return Github(token)

def post_inline_comments(repo_name, pr_number, issues):
    """
    Posts inline comments for each issue (optional, only for issues needing attention).
    """
    gh = get_github_instance()
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    for issue in issues:
        try:
            pr.create_review_comment(
                body=issue["message"],
                commit_id=pr.head.sha,
                path=issue["filename"],
                line=issue["line"],
                side="RIGHT"
            )
        except Exception as e:
            print("Could not post inline comment, will include in summary:", e)

def post_summary_comment(repo_name, pr_number, issues):
    """
    Posts a summary comment in the PR for all issues.
    """
    gh = get_github_instance()
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    if not issues:
        body = " PR Lint Bot: No issues found!"
    else:
        body = "### PR Lint Bot Summary\n"
        for issue in issues:
            body += f"- {issue['filename']}:{issue['line']} - {issue['message']}\n"

    pr.create_issue_comment(body)
