import os
from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment

def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    repo_name = os.environ.get("REPO")
    pr_number = os.environ.get("PR_NUMBER")

    if not github_token or not repo_name or not pr_number:
        print("Missing environment variables: GITHUB_TOKEN, REPO, or PR_NUMBER")
        return

    pr_number = int(pr_number)
    issues = lint_repo(".")  # Lint all .py files in repo

    post_inline_comment(repo_name, pr_number, issues)
    post_summary_comment(repo_name, pr_number, issues)

if __name__ == "__main__":
    main()
