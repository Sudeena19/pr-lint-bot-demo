import os
from lint_bot.linter import lint_repo
from lint_bot.github_bot import post_summary_comment

def main():
    issues = lint_repo(".")
    if issues:
        print("Lint issues found:")
        for i in issues:
            print(i)
        post_summary_comment(["PR Lint Bot found the following issues:"] + issues)
    else:
        print("No lint issues found!")
        post_summary_comment(["PR Lint Bot found no issues."])

if __name__ == "__main__":
    main()
