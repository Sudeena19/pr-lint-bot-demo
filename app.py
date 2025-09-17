from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment


def main():
    issues = lint_repo(".")
    print(f"Found {len(issues)} issues")

    # Try inline for each issue
    for issue in issues:
        post_inline_comment(issue)

    # Always post summary
    post_summary_comment(issues)


if __name__ == "__main__":
    main()