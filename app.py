from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_inline_comment, post_summary_comment


def main():
    issues = lint_repo(".")
    print(f"Found {len(issues)} issues")

    for issue in issues:
        if "E" in issue["message"] or "F" in issue["message"]:
            post_inline_comment(issue)

    post_summary_comment(issues)


if __name__ == "__main__":
    main()
