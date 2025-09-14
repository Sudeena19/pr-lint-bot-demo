from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment

def main():
    issues = lint_repo(".")
    print(f"Found {len(issues)} issues")

    # Post inline only for serious issues
    for issue in issues:
        if issue.get("serious"):
            post_inline_comment(issue)

    # Always post summary
    post_summary_comment(issues)

if __name__ == "__main__":
    main()
