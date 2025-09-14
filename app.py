from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment
import os

def main():
    token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")

    if not token or not repo_name or not pr_number:
        print("Missing environment variables: GITHUB_TOKEN, REPO, or PR_NUMBER")
        return

    issues = lint_repo(".")
    if issues:
        # Post first inline comment as example
        first_issue = issues[0]
        post_inline_comment(repo_name, pr_number, token, first_issue)
        # Post summary for all issues
        post_summary_comment(repo_name, pr_number, token, issues)
        print(f"Found {len(issues)} issues, posted comments.")
    else:
        post_summary_comment(repo_name, pr_number, token, ["No linting issues found!"])
        print("No issues found.")

if __name__ == "__main__":
    main()
