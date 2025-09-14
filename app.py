import os
from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment

def main():
    repo_name = os.getenv("REPO")
    pr_number = os.getenv("PR_NUMBER")
    token = os.getenv("GITHUB_TOKEN")

    if not repo_name or not pr_number or not token:
        print("Missing environment variables: GITHUB_TOKEN, REPO, or PR_NUMBER")
        return

    issues = lint_repo(".")  # Lint all Python files in repo

    # Post inline comments
    post_inline_comment(repo_name, int(pr_number), issues)

    # Post summary comment
    post_summary_comment(repo_name, int(pr_number), issues)

if __name__ == "__main__":
    main()
