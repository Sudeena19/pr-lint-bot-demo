import os
import re
from github import Github, Auth

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))

def lint_file_local(path):
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if len(line) > 100:
                    issues.append((path.replace("\\", "/"), i, f"Line too long ({len(line)} chars)"))
                if "\t" in line:
                    issues.append((path.replace("\\", "/"), i, "Contains tab instead of spaces"))
                if re.search(r"[ \t]+$", line.rstrip("\n\r")):
                    issues.append((path.replace("\\", "/"), i, "Trailing whitespace"))
    except FileNotFoundError:
        # file may not exist in workspace (rare), skip
        pass
    return issues

def build_position_map(patch):
    mapping = {}
    if not patch:
        return mapping
    pos = 0
    cur_new = None
    for raw in patch.splitlines():
        if raw.startswith('@@'):
            m = re.search(r'\+(\d+)(?:,(\d+))?', raw)
            if m:
                cur_new = int(m.group(1))
            continue
        if cur_new is None:
            continue
        pos += 1
        first = raw[:1]
        if first == ' ':
            mapping[cur_new] = pos
            cur_new += 1
        elif first == '+':
            mapping[cur_new] = pos
            cur_new += 1
        elif first == '-':
            # removed line in old file: advance old line count only (no change to cur_new)
            pass
    return mapping

def main():
    if not token or not repo_name or not pr_number:
        print("Missing environment variables: GITHUB_TOKEN, GITHUB_REPOSITORY or PR_NUMBER")
        return

    gh = Github(auth=Auth.Token(token))
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    pr_files = list(pr.get_files())
    all_issues = []
    file_position_maps = {}

    for f in pr_files:
        filename = f.filename  # path relative in repo, e.g. src/app.py
        if not filename.endswith(".py"):
            continue
        # build mapping of new-file-line -> position (used for inline comments)
        patch = getattr(f, "patch", None)
        file_position_maps[filename] = build_position_map(patch)

        # lint local file (workspace) using same relative path
        all_issues.extend(lint_file_local(filename))

    # group issues by file and attempt to create inline comments
    comments = []
    fallback = []
    for file, line, msg in all_issues:
        # normalize path form
        rel_path = file.lstrip("./")
        pos_map = file_position_maps.get(rel_path, {})
        position = pos_map.get(line)
        if position:
            comments.append({"path": rel_path, "position": position, "body": msg})
        else:
            fallback.append(f"{rel_path}:{line} {msg}")

    if comments:
        try:
            pr.create_review(body="PR Lint Bot — inline comments", event="REQUEST_CHANGES", comments=comments)
            print(f"Posted {len(comments)} inline comments.")
        except Exception as e:
            print("Failed to post inline comments, falling back to summary. Error:", e)
            # fallback to summary
            if all_issues:
                body = "PR Lint Bot found the following issues:\n\n" + "\n".join([f"{f}:{l} {m}" for f, l, m in all_issues])
                repo.create_issue_comment(pr_number, body)
                print("Posted summary comment.")
    else:
        # no inline comments possible — post summary or "no issues"
        if fallback:
            body = "PR Lint Bot found the following issues (couldn't attach inline):\n\n" + "\n".join(fallback)
            repo.create_issue_comment(pr_number, body)
            print("Posted fallback summary comment.")
        else:
            repo.create_issue_comment(pr_number, "No linting issues found.")
            print("No issues found — posted success message.")

if __name__ == "__main__":
    main()
