import os
import re

def lint_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines, start=1):
        if len(line) > 100:
            issues.append(f"{filename}:{i} Line too long ({len(line)} chars)")
        if "\t" in line:
            issues.append(f"{filename}:{i} Contains tab instead of spaces")
        if re.search(r"\s+$", line):
            issues.append(f"{filename}:{i} Trailing whitespace")
    return issues

if __name__ == "__main__":
    repo_dir = "."
    all_issues = []
    for root, _, files in os.walk(repo_dir):
        for f in files:
            if f.endswith(".py"):
                all_issues.extend(lint_file(os.path.join(root, f)))
    if all_issues:
        print("Issues found:")
        for issue in all_issues:
            print(issue)
    else:
        print("No issues found!")
