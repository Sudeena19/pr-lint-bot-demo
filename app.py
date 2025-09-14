import os
from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comments, post_summary_comment

def main():
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("PR_NUMBER")

    if not repo_name or not pr_number:
        print("Missing environment variables: GITHUB_REPOSITORY or PR_NUMBER")
        return

    pr_number = int(pr_number)
    issues = lint_repo(".")

    # Optional: post inline comments only for important issues
    post_inline_comments(repo_name, pr_number, issues)

    # Always post summary
    post_summary_comment(repo_name, pr_number, issues)

if __name__ == "__main__":
    main()
