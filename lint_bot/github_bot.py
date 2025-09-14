import os
from github import Github

def post_inline_comment(repo_name, pr_number, issues):
    """
    Post inline comments to GitHub PR.
    If API fails, fallback to summary.
    """
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    for issue in issues:
        try:
            pr.create_review(
                event="COMMENT",
                comments=[{
                    "path": issue.get("filename", "unknown"),
                    "line": issue.get("line", 1),
                    "body": issue.get("message", "")
                }]
            )
        except Exception as e:
            print(f"Could not post inline comment, will include in summary: {e}")

def post_summary_comment(repo_name, pr_number, issues):
    """
    Post a summary comment on the PR.
    """
    body = ""
    if not issues:
        body = "No lint issues found. Good job!"
    else:
        body = "### Lint issues found:\n"
        for issue in issues:
            filename = issue.get("filename", "unknown file")
            line = issue.get("line", "?")
            message = issue.get("message", "")
            body += f"- {filename}:{line} - {message}\n"

    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(body)
